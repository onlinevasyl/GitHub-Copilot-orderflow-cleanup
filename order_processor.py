import datetime
# order processor v2.3 - last updated by dave

discount_rate = 0.1  # discount

def proc(order):
    # process order
    subtotal = 0
    for item in order["items"]:
        price = item["p"]
        quantity = item["q"]
        if quantity < 0:
            quantity = 0
        if price < 0:
            price = 0
        subtotal = subtotal + (price * quantity)

    if order.get("c") == "VIP":
        # VIP discount
        subtotal = subtotal - (subtotal * discount_rate)
        subtotal = round(subtotal, 2)
    elif order.get("c") == "EMPLOYEE":
        # employee discount 20%
        subtotal = subtotal - (subtotal * 0.2)
        subtotal = round(subtotal, 2)
    elif order.get("c") == "WHOLESALE":
        subtotal = subtotal - (subtotal * 0.25)
        subtotal = round(subtotal, 2)

    # tax
    tax = subtotal * 0.08
    tax = round(tax, 2)
    subtotal = subtotal + tax
    subtotal = round(subtotal, 2)

    # build result
    result = {}
    result["order_id"] = order["id"]
    result["dt"] = str(datetime.datetime.now())
    result["sub"] = round(subtotal - tax, 2)
    result["tax"] = tax
    result["total"] = subtotal
    result["st"] = "COMPLETED"

    if subtotal > 1000:
        result["st"] = "REVIEW_REQUIRED"

    if len(order["items"]) == 0:
        result["st"] = "EMPTY"
        result["sub"] = 0
        result["tax"] = 0
        result["total"] = 0

    return result


def proc_batch(orders):
    res = []
    for o in orders:
        t = 0
        for i in o["items"]:
            p = i["p"]
            q = i["q"]
            if q < 0:
                q = 0
            if p < 0:
                p = 0
            t = t + (p * q)

        if o.get("c") == "VIP":
            t = t - (t * discount_rate)
            t = round(t, 2)
        elif o.get("c") == "EMPLOYEE":
            t = t - (t * 0.2)
            t = round(t, 2)
        elif o.get("c") == "WHOLESALE":
            t = t - (t * 0.25)
            t = round(t, 2)

        tax = t * 0.08
        tax = round(tax, 2)
        t = t + tax
        t = round(t, 2)

        r = {}
        r["order_id"] = o["id"]
        r["dt"] = str(datetime.datetime.now())
        r["sub"] = round(t - tax, 2)
        r["tax"] = tax
        r["total"] = t
        r["st"] = "COMPLETED"

        if t > 1000:
            r["st"] = "REVIEW_REQUIRED"

        if len(o["items"]) == 0:
            r["st"] = "EMPTY"
            r["sub"] = 0
            r["tax"] = 0
            r["total"] = 0

        res.append(r)
    return res


def gen_report(results):
    # print report
    s = "ORDER REPORT\n"
    s = s + "=" * 40 + "\n"
    tt = 0
    for r in results:
        s = s + "Order: " + str(r["order_id"]) + " | Total: $" + str(r["total"]) + " | Status: " + r["st"] + "\n"
        tt = tt + r["total"]
    s = s + "=" * 40 + "\n"
    s = s + "Grand Total: $" + str(round(tt, 2)) + "\n"
    s = s + "Orders: " + str(len(results)) + "\n"
    return s



# === CODE REVIEW NOTES === 

# 1. Variable names: d, o, t, p, q, r, s, tt — all cryptic, single-letter 

# 2. proc() and proc_batch() contain nearly identical logic (copy-paste duplication) 

# 3. Discount rates are hardcoded magic numbers (0.1, 0.2, 0.25) 

# 4. Tax rate (0.08) is a magic number buried in logic 

# 5. No docstrings, no type hints, no meaningful comments 

# 6. Empty order check happens AFTER calculation (wrong order of operations) 

# 7. gen_report() uses string concatenation instead of f-strings or templates 

# 8. No unit tests exist 

# 9. No README or module-level documentation 