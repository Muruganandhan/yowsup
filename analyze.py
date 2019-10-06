from datetime import datetime

import plotly.figure_factory as ff
import re

def parse_data():
    # s = 'I 2019-10-05 14:32:25,583 yowsup.demos.presence.layer - |K7-offline: 1570266145.58|'
    with open('20191005-1.log', 'r') as f:
        s = f.read()
        # matchs = re.findall('(\|.*\|)', s)
        matchs = re.findall('\|(.*)\|', s)
        data = {}
        temp_dict = {}
        for match in matchs:
            name, temp = match.split('-')
            state, t = temp.split(':')
            if state == "online":
                temp_dict[name] = [t]
            else:
                start = temp_dict.get(name)
                if start:
                    start = start.pop()
                    start = datetime.fromtimestamp(float(start))
                    t = datetime.fromtimestamp(float(t))
                    if name not in data:
                        data[name] = [(start, t)]
                    else:
                        data[name].append((start, t))
            # data.append((name, state, t))
        # print(data)
        return data

def main():
    data = parse_data()
    df = []
    for name, online_ranges in data.items():
        for online_range in online_ranges:
            df.append({
                "Task": name,
                "Start": online_range[0],
                "Finish": online_range[1],
                "Resource": "Online"
            })
    colors = {
        'Online': 'rgb(0, 255, 100)'
    }
    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                      group_tasks=True, title="WA Online Chart")
    fig.show()


if __name__ == "__main__":
    main()