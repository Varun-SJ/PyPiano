import mido


def decode(file, time_interval=20):
    if isinstance(file, mido.MidiFile):
        print("Input is mido file")
    if isinstance(file, str):
        print("Input is string")
        file = mido.MidiFile(file)

    time = 0

    per_key_dict = {}
    tuple_times = []
    on_times = []
    off_times = []
    time_array = []

    for msg in file:
        if hasattr(msg, "time"):
            time += msg.time
            if hasattr(msg, "note"):
                if msg.note not in per_key_dict.keys():
                    per_key_dict[msg.note] = {"on": [], "off": [], "tuple": []}
                if msg.type == "note_on":
                    per_key_dict[msg.note]["on"].append(time)
                    on_times.append((time, msg.note))
                if msg.type == "note_off":
                    per_key_dict[msg.note]["off"].append(time)
                    on = per_key_dict[msg.note]["on"][-1]
                    per_key_dict[msg.note]["tuple"].append((on, time))
                    tuple_times.append((on, time, msg.note))
                    off_times.append((time, msg.note))

    pressed = []
    for x in range(int(file.length) * time_interval):
        time = x * (1 / time_interval)
        for key, val in per_key_dict.items():
            for tim in val["tuple"]:
                if tim[0] <= time <= tim[1]:
                    pressed.append(key)
        time_array.append(pressed)
        pressed = []

    tuple_times.sort()

    return per_key_dict, tuple_times, on_times, off_times, time_array
