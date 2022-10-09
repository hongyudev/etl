def transform_row(env, row):
    """return a dictionary where each k:v pair is a transformed column"""
    output = {}
    rewrite_fns = env.rewrite_fns
    success = True
    for k, v in row.items():
        if k in rewrite_fns:
            rewritten = rewrite_fns[k](v, env.metric)
            if len(rewritten) == 0:
                success = False
        else:
            rewritten = {k: v}
        output = output | rewritten
    if success:
        env.metric.success += 1
        return output
    env.metric.failure += 1
    return {}
