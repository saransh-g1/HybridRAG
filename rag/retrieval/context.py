def build_context(results):

    context = []

    for result in results:

        context.append(
            result.payload["text"]
        )

    return "\n\n".join(context)