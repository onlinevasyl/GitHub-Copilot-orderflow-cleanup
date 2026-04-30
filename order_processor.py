import datetime
# order processor v2.3 - last updated by dave

d = 0.1  # discount

def proc(o):
    # process order
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
        # VIP discount
        t = t - (t * d)
        t = round(t, 2)
    elif o.get("c") == "EMPLOYEE":
        # employee discount 20%
        t = t - (t * 0.2)
        t = round(t, 2)
    elif o.get("c") == "WHOLESALE":
        t = t - (t * 0.25)
        t = round(t, 2)

    # tax
    tax = t * 0.08
    tax = round(tax, 2)
    t = t + tax
    t = round(t, 2)

    # build result
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

    return r


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
            t = t - (t * d)
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
