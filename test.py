from order_processor import proc, proc_batch, gen_report

order = {
    "id": 1001,
    "items": [{"p": 29.99, "q": 2}, {"p": 9.99, "q": 1}],
    "c": "VIP"
}
result = proc(order)
print(result)
print(gen_report([result]))
