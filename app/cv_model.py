from PIL import Image
from transformers import pipeline
from typing import Dict, List, Callable
import sys
from flet import Page
import functools


# async def task_model_computation(path: str, query: str) -> List[Dict[str, str | float]]:
def task_model_computation(
    path: str, query: str, callback: Callable[..., None] | None = None
) -> List[Dict[str, str | float]] | None:
    if path and query:
        vqa_pipeline = pipeline(
            task="visual-question-answering",
            model="dandelin/vilt-b32-finetuned-vqa",
        )
        # NOTE
        # [{'score': 0.9998154044151306, 'answer': 'yes'}]
        answer = vqa_pipeline(Image.open(path).convert(mode="RGB"), query, top_k=3)
        # FIXME
        # This is delicate code
        if callback:
            callback(answer[0].get("answer"))  # noqa
        print(f"DEBUG:{answer=}, {path=}, {query=}")
        return answer


def model_computation(
    path: str,
    query: str,
    app_context: Page | None = None,
    error_callback: Callable[..., None] | None = None,
    success_callback: Callable[..., None] | None = None,
    extra_callback: Callable[..., None] | None = None,
) -> List[str] | None:
    if not path and query:
        return None
    try:
        query_result_set = []
        if app_context:
            # query_result_set = app_context.run_task(
            #     functools.partial(task_model_computation, path, query)
            # )
            app_context.run_thread(
                task_model_computation,
                path,
                query,
                extra_callback,
            )
        else:
            query_result_set = task_model_computation(path=path, query=query)
    except Exception as e:
        print("ERROR", e)
        # NOTE
        # We could be more granular here
        if not app_context:
            raise RuntimeError(
                "Something went wrong when trying to load the model/image"
            )
        if app_context and error_callback:
            # NOTE
            # We expect the callback to be a flet.Control
            # app_context.open(callback)
            error_callback()
    else:
        # FIXME
        # This is getting messy
        # run_task needs an async def
        # run_task returs Future
        # Future.result() throws
        # return [result.get("answer") for result in query_result_set.result()]
        if app_context and success_callback:
            success_callback()
        return query_result_set


if __name__ == "__main__":
    try:
        ans = model_computation(sys.argv[1], sys.argv[2])
    except IndexError as e:
        raise ValueError(
            "Please run it with", __file__, "<path-to-an-image>", "<query>"
        ) from e
    else:
        print(ans)
