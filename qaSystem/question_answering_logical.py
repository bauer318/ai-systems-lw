from InquirerPy import inquirer

from qaSystem.question_answering_manager import QuestionAnsweringManager
from qaSystem.request import Request
from qaSystem.test_processing import creates_request
from reader import get_dataset_array

current_request: Request


def process_request(request: Request, text: str):
    global current_request

    if request.and_log:
        texts = text.lower().split(" и ")
        data = []
        for text_elem in texts:
            qa_system = QuestionAnsweringManager()
            current_request = creates_request(text_elem)
            current_request = completes_request(current_request, request)
            qa_system.request = current_request
            qa_system.data = get_dataset_array()
            qa_system.find_by_tags()
            data = merges_data(qa_system.data, data, True)
        print_final(data)
    elif request.or_log:
        texts = text.lower().split(" или ")
        data = []
        for text_elem in texts:
            qa_system = QuestionAnsweringManager()
            current_request = creates_request(text_elem)
            current_request = completes_request(current_request, request)
            qa_system.request = current_request
            qa_system.data = get_dataset_array()
            qa_system.find_by_tags()
            data = merges_data(qa_system.data, data, False)
        if current_request.num_ == "One":
            data = data[:1]
        print_final(data)
    else:
        qa_system = QuestionAnsweringManager()
        qa_system.request = request
        qa_system.data = get_dataset_array()
        qa_system.find_by_tags()
        if qa_system.request.num_ == "One":
            qa_system.data = qa_system.data[:1]
        qa_system.print("Result")


def print_final(data: []):
    qa_system = QuestionAnsweringManager()
    qa_system.data = data

    qa_system.print("Result")


def merges_data(current_data: [], old_data: [], is_and: bool):
    result = []
    if len(current_data) == 0:
        return old_data
    if len(old_data) == 0:
        return current_data
    if is_and:
        for old_item in old_data:
            for current_item in current_data:
                if current_item.name == old_item.name:
                    result.append(old_item)
                    break
    else:
        for old_item in old_data:
            result.append(old_item)
            for current_item in current_data:
                if current_item.name != old_item.name and not_in(current_item.name, result):
                    result.append(current_item)
    return result


def not_in(item, source_array: []) -> bool:
    for elem in source_array:
        if item == elem.name:
            return False
    return True


def completes_request(current_request_: Request, source_request: Request) -> Request:
    current_request_.show = set_attribute(current_request_.show, source_request.show)
    if (current_request_.num_ == "One" and source_request.num_ != "One") or (
            current_request_.num_ != "One" and source_request.num_ == "One"):
        current_request_.num_ = "Many"
    return current_request_


def set_attribute(current, source):
    if current is None and source is not None:
        current = source
    return current


def loop_main() -> int:
    options = ["Введите вопрос", "Выход"]
    selected_menu = inquirer.select(
        message="",
        choices=options
    ).execute()
    if selected_menu == "Введите вопрос":
        text = input("Вопрос: ")
        request = creates_request(text)
        process_request(request, text)
        return 0
    else:
        return 1
