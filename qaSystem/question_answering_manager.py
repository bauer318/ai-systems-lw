from datasetitem import DatasetItem
from qaSystem.request import Request
from util import get_motorcycle_type, convert_value


class QuestionAnsweringManager:
    data: [] = None
    request: Request = None

    def search_motorcycles(self) -> []:
        result: []
        if self.request.show:
            request_ = self.request
            for item in self.data:
                if request_.color is not None:
                    if item.color == request_.color:
                        result.append(item)
        return result

    def find_by_color(self):
        result = []
        request_ = self.request
        if request_.color is None:
            return self.get_result(self.data)
        for item in self.data:
            if request_.color is not None and item.color == request_.color:
                result.append(item)

        res = self.get_result(result)
        # self.print("Color")
        return res

    def get_result(self, result: []):
        self.data = result
        return self.data

    def find_by_type(self):
        current_data = self.find_by_color()
        result = []
        if self.request.type is None:
            return self.get_result(current_data)
        for item in current_data:
            motorcycle_type = get_motorcycle_type(item)
            match self.request.type:
                case 'road':
                    if (motorcycle_type == "Cruiser" or
                            motorcycle_type == "Sport Motorcycle" or
                            motorcycle_type == "Sport Tourer"):
                        result.append(item)
                case 'off-road':
                    if (motorcycle_type == "Enduro" or
                            motorcycle_type == "Motocross"):
                        result.append(item)
                case 'dual-sport':
                    if motorcycle_type == "Touring Motorcycle":
                        result.append(item)

        res = self.get_result(result)
        # self.print("Type")
        return res

    def find_by_weight(self):
        current_data = self.find_by_type()
        result = []
        if self.request.min_weight is None and self.request.max_weight is None:
            return self.get_result(current_data)

        for item in current_data:
            if self.request.min_weight is not None:
                if self.request.max_weight is not None:
                    if self.request.min_weight <= convert_value(item.weight) <= self.request.max_weight:
                        result.append(item)
                else:
                    if self.request.min_weight <= convert_value(item.weight):
                        result.append(item)
            elif self.request.max_weight is not None:
                if self.request.max_weight >= convert_value(item.weight):
                    result.append(item)

        res = self.get_result(result)

        # self.print("Weight")
        return res

    def find_by_tags(self):
        if self.request.show:
            current_data = self.find_by_weight()
            result = []
            return self.perfom_by_tags(current_data, result)

    def transmission_case(self, tag_value, current_data: [], result: []):
        for item in current_data:
            if self.request.exist:
                if item.transmission == tag_value:
                    result.append(item)
            else:
                if item.transmission != tag_value:
                    result.append(item)

    def height_case(self, tag_value, current_data: [], result: []):
        for item in current_data:
            if self.request.extr is not None:
                if self.request.extr == "Max":
                    if convert_value(item.height) <= tag_value:
                        result.append(item)
                else:
                    if convert_value(item.height) >= tag_value:
                        result.append(item)
            else:
                if convert_value(item.height) == tag_value:
                    result.append(item)

    def engine_capacity_case(self, tag_value, current_data: [], result: []):
        for item in current_data:
            if self.request.extr is not None:
                if self.request.extr == "Max":
                    if item.engine_capacity <= tag_value:
                        result.append(item)
                else:
                    if item.engine_capacity >= tag_value:
                        result.append(item)
            else:
                if item.engine_capacity == tag_value:
                    result.append(item)

    def exist_turn_signal_case(self, current_data: [], result: []):
        for item in current_data:
            if self.request.exist:
                if item.exist_turn_signal:
                    print(item.name)
                    result.append(item)
            else:
                if not item.exist_turn_signal:
                    result.append(item)

    def perfom_by_tags(self, current_data: [], result: []):
        if len(self.request.tags.keys()) == 0:
            return self.get_result(current_data)
        for tag in self.request.tags.keys():
            tag_value = self.request.tags[tag]
            match tag:
                case 'transmission':
                    print('transmission')
                    self.transmission_case(tag_value, current_data, result)
                case 'height':
                    print('height')
                    self.height_case(tag_value, current_data, result)
                case 'engine_capacity':
                    print('capacity')
                    self.engine_capacity_case(tag_value, current_data, result)
                case 'exist_turn_signal':
                    self.exist_turn_signal_case(current_data, result)

        res = self.get_result(result)
        return res

    def print(self, title: str):
        print(f"\n===={title}=====")
        if self.data:
            for item in self.data:
                print(item.name, f'Масса: {item.weight} Цвет: {item.color} Объем двигателя: {item.engine_capacity}')
        else:
            print("Empty")
