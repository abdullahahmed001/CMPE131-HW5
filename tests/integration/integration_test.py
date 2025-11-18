from src.order_io import load_order
from src.order_io import write_receipt
import pytest

def test_order_integration(tmp_path):
    input_file = tmp_path / "order.csv"
    input_file.write_text("apple,$2.50\nbanana,1.25\n", encoding="utf-8")
    items = load_order(input_file)

    write_receipt(tmp_path / "receipt.txt", items, discount_percent=6, tax_rate=0.2)
    output_text = (tmp_path / "receipt.txt").read_text(encoding="utf-8")

    assert "apple: $2.50" in output_text
    assert "banana: $1.25" in output_text
    assert "TOTAL: " in output_text
