def get_custom_labeling_fun(prefix="", suffix="", show_counter=True, show_rate=True, show_remaining_time=True, show_elapsed_time=True):
    templates = []

    for size_enabled in (False, True):
        template_parts = []
        if show_counter:
            template_parts.append("{index} / {size} items" if size_enabled else "{index} items")

        if show_rate:
            template_parts.append("Rate {rate}/{rate_metric}")

        if show_remaining_time and size_enabled:
            template_parts.append("Remaining {remaining}s")

        if show_elapsed_time:
            template_parts.append("Elapsed {elapsed:.1f}s")

        template_parts = [
            "{prefix}" if prefix else "",
            " . ".join(template_parts),
            "{suffix}" if suffix else ""
        ]
        template = " | ".join(part for part in template_parts if len(part))

        templates.append(template)

        del template_parts

    def _labeling_fun(index, size, elapsed):
        ratio = (1.0 * index / elapsed) if index else None
        use_kseconds = (ratio < 10 and ratio is not None)

        return (templates[1 if size else 0]).format(
            index=index,
            size=size or "?",
            rate=int((1000.0 if use_kseconds else 1.0) * ratio) if index else "?",
            rate_metric=("1000s" if use_kseconds else "s"),
            remaining=int((size-index) / ratio) if (size and index) else "?",
            elapsed=elapsed,
            prefix=prefix,
            suffix=suffix
        )
    return _labeling_fun
