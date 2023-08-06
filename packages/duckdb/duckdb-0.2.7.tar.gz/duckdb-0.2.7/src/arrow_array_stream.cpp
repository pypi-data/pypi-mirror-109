#include "duckdb/common/assert.hpp"
#include "include/duckdb_python/arrow_array_stream.hpp"
#include "duckdb/common/common.hpp"

namespace duckdb {

PythonTableArrowArrayStream::PythonTableArrowArrayStream(PyObject *arrow_table_p,
                                                         PythonTableArrowArrayStreamFactory *factory)
    : factory(factory), arrow_table(arrow_table_p), chunk_idx(0) {
	stream = make_unique<ArrowArrayStreamWrapper>();
	InitializeFunctionPointers(&stream->arrow_array_stream);
	py::handle table_handle(arrow_table_p);
	batches = table_handle.attr("to_batches")();
	py::int_ num_rows_func = -1;
	if (py::hasattr(table_handle, "num_rows")) {
		num_rows_func = table_handle.attr("num_rows");
	}
	stream->number_of_rows = num_rows_func;

	stream->arrow_array_stream.private_data = this;
}

void PythonTableArrowArrayStream::InitializeFunctionPointers(ArrowArrayStream *stream) {
	stream->get_schema = PythonTableArrowArrayStream::GetSchema;
	stream->get_next = PythonTableArrowArrayStream::GetNext;
	stream->release = PythonTableArrowArrayStream::Release;
	stream->get_last_error = PythonTableArrowArrayStream::GetLastError;
}

unique_ptr<ArrowArrayStreamWrapper> PythonTableArrowArrayStreamFactory::Produce(uintptr_t factory_ptr) {
	py::gil_scoped_acquire acquire;
	PythonTableArrowArrayStreamFactory *factory = (PythonTableArrowArrayStreamFactory *)factory_ptr;
	if (!factory->arrow_table) {
		return nullptr;
	}
	//! This is a bit hacky, but has to be this way to hide pybind from the main duckdb lib
	auto table_stream = new PythonTableArrowArrayStream(factory->arrow_table, factory);
	return move(table_stream->stream);
}

int PythonTableArrowArrayStream::PythonTableArrowArrayStream::GetSchema(ArrowArrayStream *stream,
                                                                        struct ArrowSchema *out) {
	D_ASSERT(stream->private_data);
	py::gil_scoped_acquire acquire;
	auto my_stream = (PythonTableArrowArrayStream *)stream->private_data;
	if (!stream->release) {
		my_stream->last_error = "stream was released";
		return -1;
	}
	py::handle table_handle(my_stream->arrow_table);
	auto schema = table_handle.attr("schema");
	if (!py::hasattr(schema, "_export_to_c")) {
		my_stream->last_error = "failed to acquire export_to_c function";
		return -1;
	}
	auto export_to_c = schema.attr("_export_to_c");
	export_to_c((uint64_t)out);
	return 0;
}

int PythonTableArrowArrayStream::GetNext(struct ArrowArrayStream *stream, struct ArrowArray *out) {
	D_ASSERT(stream->private_data);
	py::gil_scoped_acquire acquire;
	auto my_stream = (PythonTableArrowArrayStream *)stream->private_data;
	if (!stream->release) {
		my_stream->last_error = "stream was released";
		return -1;
	}
	if (my_stream->chunk_idx >= py::len(my_stream->batches)) {
		out->release = nullptr;
		return 0;
	}
	auto stream_batch = my_stream->batches[my_stream->chunk_idx++];
	if (!py::hasattr(stream_batch, "_export_to_c")) {
		my_stream->last_error = "failed to acquire export_to_c function";
		return -1;
	}
	auto export_to_c = stream_batch.attr("_export_to_c");
	export_to_c((uint64_t)out);
	return 0;
}

void PythonTableArrowArrayStream::Release(struct ArrowArrayStream *stream) {
	py::gil_scoped_acquire acquire;
	if (!stream->release) {
		return;
	}
	stream->release = nullptr;
	auto private_data = (PythonTableArrowArrayStream *)stream->private_data;
	delete (PythonTableArrowArrayStream *)stream->private_data;
}

const char *PythonTableArrowArrayStream::GetLastError(struct ArrowArrayStream *stream) {
	if (!stream->release) {
		return "stream was released";
	}
	D_ASSERT(stream->private_data);
	auto my_stream = (PythonTableArrowArrayStream *)stream->private_data;
	return my_stream->last_error.c_str();
}
} // namespace duckdb