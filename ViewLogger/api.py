def fetchChangesAPI(changes):
    rows = []
    for change in changes:
        row = {}
        row["done_on"] = change.done_on
        row["done_by"] = change.done_by
        row["view_name"] = change.view_name
        row["id"] = change.id
        row['url'] = change.url
        row['view_args'] = change.view_args
        row['view_kwargs'] = change.view_kwargs
        reqBody = {}
        if change.request_body:
            for k in change.request_body:
                if len(change.request_body[k]) > 0: reqBody[k] = change.request_body[k]
        row['request_body'] = reqBody
        row['request_method'] = change.request_method
        rows.append(row)
    count = len(rows)
    res = {"count": count, "changes": rows}
    return res
