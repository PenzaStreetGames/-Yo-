from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.types_control import write, display, shift, read
from yovirmac.modules.segment_control import init, change, find, show, put, take
from yovirmac.modules.tape_control import (add, view, setting, extend, get,
                                           make, append, pull)
from yovirmac.modules.segment_control.functions import *
from yovirmac.modules.object_control import link, draw
from yovirmac.modules.upper_commands import math
import random


def cell_overflow_write():
    """Проверка на переполнение путём записи больших значений"""
    value = 1
    for i in range(capacity + 4):
        write.cell(0, value)
        display.cell(0)
        value <<= 1
        value += 1


def cell_overflow_shift():
    """Проверка на переполнение путём битового сдига влево"""
    write.cell(0, 1)
    for i in range(capacity + 4):
        display.cell(0)
        shift.left(0, 1)
        write.bit(0, 0, 1)


def bit_writing():
    """Проверка на запись бита в ячейку"""
    write.clean(0)
    for i in range(capacity + 4):
        write.bit(0, i, 1)
        display.cell(0)
        write.bit(0, i, 0)


def number_writing():
    """Проверка на запись числа в ячейку"""
    write.clean(0)
    for i in range(20):
        number = random.randint(0, 2 ** 32 - 1)
        print(number)
        write.number(0, number)
        display.cell(0)


def type_writing():
    """Проверка на запись типа в ячеку"""
    for kind in types:
        write.kind(0, type)
        print(read.kind(0))
        display.cell(0)


def logic_writing():
    """Проверка на запись логических величин"""
    values = [0, 1, 2]
    for value in values:
        write.logic(0, value)
        print(value, read.logic(0))


def string_writing():
    """Проверка на запись введённой строки"""
    value = input()
    write.chars(0, value)
    for i in range(len(value) + 1):
        print(read.cell(i), read.char(i))
    print(read.chars(0))


def command_writing():
    """Проверка на запись команды"""
    for i in range(0, len(commands) + 1):
        try:
            write.command(0, i)
            display.command(0)
        except LowerCommandError as error:
            print(error)
    print()
    for abbrev in commands_abbreviation:
        write.command(0, abbrev)
        display.command(0)
    try:
        write.command(0, "no_command")
        display.command(0)
    except LowerCommandError as error:
        print(error)


def entity_writing():
    """Проверка на запись объектов"""
    entities = [
        [0, "none", None],
        [0, "link", 1000],
        [0, "command", 15],
        [0, "logic", 1],
        [0, "number", 255],
        [0, "chars", "something"]
    ]
    for entity in entities:
        write.entity(*entity)
        display.cell(0)
        display.cell(1)
        display.entity(0)


def header_part_writing():
    """Проверка на запись части заголовка"""
    for header_type in seg_header.keys():
        write.header_part(0, header_type, {})
        display.header_part(0, header_type)
        for i in range(header_part_length):
            display.cell(i)
            write.clean(i)
        print()


def header_writing():
    """Проверка на запись заголовка"""
    for header_type in seg_header.keys():
        if header_type == "basic":
            continue
        write.header(0, {"type": seg_types.index(header_type)}, {})
        display.header(0)
        print()


def attribute_writing():
    """Проверка на изменение атрибута"""
    add.system_area()
    display.segment(0)
    show.attribute(0, "segment_end")
    show.attribute(0, "memory_stack")
    print()
    change.attribute(0, "segment_end", 64)
    display.segment(0)
    show.attribute(0, "segment_end")
    print()
    change.attribute(0, "memory_stack", 32)
    display.segment(0)
    show.attribute(0, "memory_stack")
    print()


def stack_writing():
    """Проверка на запись стеков"""
    add.system_area()
    add.memory_stack()
    add.call_stack()
    view.tape()


def dictionary_item_writing():
    """Проверка на запись элемента списка"""
    args = [128, 64, 256]
    write.entity(0, "dictionary_item", args)
    display.entity(0)
    change.dictionary_item_part(0, "key", 48)
    display.entity(0)


def data_segment_writing():
    """Проверка на запись сегмента данных"""
    add.system_area()
    add.memory_stack()
    add.call_stack()
    add.data_segment()
    view.tape()


def program_writing():
    """Проверка на запись программы"""
    add.system_area()
    add.memory_stack()
    add.call_stack()
    add.data_segment()
    add.program("program.yovc")
    view.tape()
    program = find.attribute(seg_links["system"], "main_program")
    show.attribute(seg_links["system"], "target_cell")
    show.program_code(program)


def array_writing():
    """Проверка на запись массива"""
    write.entity(0, "array", [5, 10, 15, 20, 25])
    display.entity(0)


def command_with_args_writing():
    """Проверка на запись команды с аргументами"""
    write.command_with_args(0, "Crt", [{"type": "array", "value": [5, 10, 20]}])
    display.command_with_args(0)
    write.command_with_args(0, "Fnd", [{"type": "chars", "value": "line"}])
    display.command_with_args(0)
    write.command_with_args(0, "Add", [{"type": "link", "value": 16},
                                       {"type": "link", "value": 22}])
    display.command_with_args(0)


def list_segment_writing():
    """Проверка на запись сегмента списка"""
    setting.initialisation("program.yovc")
    add.list_segment()
    view.tape()


def segment_extending():
    """Проверка на расширение сегментов"""
    segment_nums = setting.initialisation("program.yovc")
    list_num = add.list_segment()
    namespace_num = find.attribute(seg_links["system"], "target_namespace")
    data_num = find.attribute(seg_links["system"], "first_data_segment")
    extend.data_segment(data_num)
    extend.namespace(namespace_num)
    extend.list_segment(list_num)
    view.tape()


def stack_taking_putting():
    """Проверка на заполнение и опустошение стека"""
    real_memory_stack_size = minimal_data_length["memory_stack"]
    minimal_data_length["memory_stack"] = 8
    setting.initialisation("program.yovc")
    num = find.attribute(seg_links["system"], "memory_stack")
    data = [5, 10, 15, 20, 25]
    print("Заполнение:")
    for i in range(len(data)):
        try:
            put.stack(num, "link", data[i])
            show.segment_body(num)
        except LowerCommandError as error:
            print(error)
    print("Извлечение:")
    for i in range(len(data)):
        try:
            obj_type, obj_value = take.stack(num)
            show.segment_body(num)
        except LowerCommandError as error:
            print(error)
    show.segment_body(num)
    minimal_data_length["memory_stack"] = real_memory_stack_size


def data_segment_putting():
    """Проверка на заполнение сегмента данных"""
    real_data_segment_size = minimal_data_length["data_segment"]
    minimal_data_length["data_segment"] = 4
    setting.initialisation("program.yovc")
    num = find.attribute(seg_links["system"], "first_data_segment")
    put.data_segment(num, "chars", "Эта строка не влезет в маленький сегмент")
    put.data_segment(num, "dictionary_item", [15, 20, 25])
    put.data_segment(num, "number", 255)
    view.tape()
    view.data_segment()
    minimal_data_length["data_segment"] = real_data_segment_size


def string_segment_putting():
    """Проверка на заполнение сегмента строки"""
    real_string_segment_size = minimal_data_length["string_segment"]
    minimal_data_length["string_segment"] = 4
    setting.initialisation("program.yovc")
    num = add.string_segment()
    put.string_segment(num, "char_list",
                       "Эта строка не влезет в маленький сегмент")
    view.tape()
    print(get.string_segment(num))
    view.string_segment(num)
    minimal_data_length["string_segment"] = real_string_segment_size


def list_segment_putting():
    """Проверка на заполнение сегмента списка"""
    real_list_segment_size = minimal_data_length["list_segment"]
    minimal_data_length["list_segment"] = 4
    setting.initialisation("program.yovc")
    num = add.list_segment()
    put.list_segment(num, "link_list", [i for i in range(40)])
    view.tape()
    print(get.list_segment(num))
    view.list_segment(num)
    minimal_data_length["list_segment"] = real_list_segment_size


def namespace_putting():
    """Проверка на заполнение пространства имён"""
    real_namespace_size = minimal_data_length["namespace"]
    minimal_data_length["namespace"] = 4
    setting.initialisation("program.yovc")
    prog_num = find.attribute(seg_links["system"], "main_program")
    num = add.namespace(prog_num)
    put.namespace(num, "link_list", [i for i in range(40)])
    view.tape()
    print(get.namespace(num))
    view.namespace(num)
    minimal_data_length["namespace"] = real_namespace_size


def list_and_string_segments_making():
    """Проверка на создание сегментов строки и списка с данными"""
    setting.initialisation("program.yovc")
    str_num = make.string_segment("Эта строка должна влезть")
    list_num = make.list_segment([i for i in range(40)])
    view.tape()
    view.string_segment(str_num)
    view.list_segment(list_num)


def negative_number_writing():
    """Проверка на запись отрицательного числа"""
    value = -1
    for i in range(capacity + 4):
        write.signed_cell(0, value)
        display.signed_cell(0)
        value *= 2
    print()
    value = 1
    for i in range(capacity + 4):
        write.signed_cell(0, value)
        display.signed_cell(0)
        value <<= 1
        value += 1


def negative_command_working():
    """Проверка работы команды Negative"""
    setting.initialisation("program.yovc")
    number = -255
    print("number", number)
    num = append.data_segment("number", number)
    math.Negative(num)
    kind, number = link.memory_stack_get()
    print(kind, number)


def math_operations_working():
    """Проверка работы математических операций"""
    setting.initialisation("program.yovc")
    number_1 = 97
    number_2 = -65
    num_1 = append.data_segment("number", number_1)
    num_2 = append.data_segment("number", number_2)
    print(f"Negative: - {number_1}")
    math.Negative(num_1)
    draw.memory_stack_link()
    print(f"Add: {number_1} + {number_2}")
    math.Add(num_1, num_2)
    draw.memory_stack_link()
    print(f"Increment: {number_1}++")
    math.Increment(num_1)
    draw.memory_stack_link()
    print(f"Decrement: {number_1}--")
    math.Decrement(num_1)
    draw.memory_stack_link()
    print(f"Subtract: {number_1} - {number_2}")
    math.Subtract(num_1, num_2)
    draw.memory_stack_link()
    print(f"Multiply: {number_1} * {number_2}")
    math.Multiply(num_1, num_2)
    draw.memory_stack_link()
    print(f"Divide: {number_1} / {number_2}")
    math.Divide(num_1, num_2)
    draw.memory_stack_link()
    print(f"Modulo: {number_1} % {number_2}")
    math.Modulo(num_1, num_2)
    draw.memory_stack_link()
