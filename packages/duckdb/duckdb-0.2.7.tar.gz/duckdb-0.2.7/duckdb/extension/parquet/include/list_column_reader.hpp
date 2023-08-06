//===----------------------------------------------------------------------===//
//                         DuckDB
//
// list_column_reader.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "column_reader.hpp"
#include "templated_column_reader.hpp"

namespace duckdb {

class ListColumnReader : public ColumnReader {
public:
	ListColumnReader(ParquetReader &reader, LogicalType type_p, const SchemaElement &schema_p, idx_t schema_idx_p,
	                 idx_t max_define_p, idx_t max_repeat_p, unique_ptr<ColumnReader> child_column_reader_p);

	idx_t Read(uint64_t num_values, parquet_filter_t &filter, uint8_t *define_out, uint8_t *repeat_out,
	           Vector &result_out) override;

	virtual void Skip(idx_t num_values) override {
		D_ASSERT(0);
	}

	void IntializeRead(const std::vector<ColumnChunk> &columns, TProtocol &protocol_p) override {
		child_column_reader->IntializeRead(columns, protocol_p);
	}

	idx_t GroupRowsAvailable() override {
		return child_column_reader->GroupRowsAvailable();
	}

private:
	unique_ptr<ColumnReader> child_column_reader;
	ResizeableBuffer child_defines;
	ResizeableBuffer child_repeats;
	uint8_t *child_defines_ptr;
	uint8_t *child_repeats_ptr;

	Vector child_result;
	parquet_filter_t child_filter;
	DataChunk append_chunk;

	Vector overflow_child_vector;
	idx_t overflow_child_count;
};

} // namespace duckdb
