# project: p4
# submitter: cdunteman
# partner: none

import click, zipfile, csv, io, socket, struct, geopandas, re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
from io import TextIOWrapper
from operator import itemgetter
from collections import defaultdict

def zip_csv_iter(name):
    with ZipFile(name) as zf:
        with zf.open(name.replace(".zip", ".csv")) as f:
            reader = csv.reader(TextIOWrapper(f))
            for row in reader:
                yield row
                
def ip2long(ip):
    """
    Convert an IP string to long
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]
# https://stackoverflow.com/questions/9590965/convert-an-ip-string-to-a-number-and-vice-versa

@click.command()
@click.argument('zip1')
@click.argument('zip2')
@click.argument('mod', type=click.INT)
def sample(zip1, zip2, mod):
    reader = zip_csv_iter(zip1)
    header = next(reader)
    ip_idx = header.index("ip")
    idx = 0
    csv_file = zip2.replace(".zip", ".csv")
    
    with ZipFile(zip2, "w", compression = ZIP_DEFLATED) as zf:
        with zf.open(csv_file, "w") as raw:
            with TextIOWrapper(raw) as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for row in reader:
                    # print(row[ip_idx])
                    # based on stride write rows
                    if idx % mod == 0:
                        writer.writerow(row)
                    idx += 1 
                    
@click.command()
@click.argument('zip1')
@click.argument('zip2')
def sort(zip1, zip2):
    new_rows = []
    reader = zip_csv_iter(zip1)
    header = next(reader)
    rows = list(reader)
    for row in rows:
        new_row = []
        new_ip = fix_ip(row[0])
        new_row.append(new_ip)
        new_row.extend(row)
        new_rows.append(new_row)
    orig_rows = []
    new_rows = sorted(new_rows, key = itemgetter(0))
    for row in new_rows:
        orig_rows.append(row[1:])
    csv_file = zip2.replace("zip", "csv")
    with ZipFile(zip2, "w", compression = ZIP_DEFLATED) as zf:
        with zf.open(csv_file, "w") as raw:
            with TextIOWrapper(raw) as f:
                writer = csv.writer(f)
                writer.writerow(header)
                if row != None:
                    pass
                for row in orig_rows:
                    writer.writerow(row)  
                    
def fix_ip(val):
    ip  = re.sub('[^\d\.]', '0', val)
    new_ip = ip2long(ip)
    return new_ip

@click.command()
@click.argument('zip1')
@click.argument('zip2')
def country(zip1, zip2):
    with ZipFile("IP2LOCATION-LITE-DB1.CSV.ZIP", 'r') as zips:
        all_files = zips.namelist()
        for file_name in all_files:
            file = file_name.upper()
            if file.endswith('.CSV'):
                zips.extract(file_name)
                with open(file_name) as f:
                    reader = csv.reader(f)
                    coutry_list = list(reader)
                    
    
    values = zip_csv_iter(zip1)
    header = next(values)
    header.append("country")
    
    csv_file = zip2.replace("zip", "csv")
    with ZipFile(zip2, "w", compression = ZIP_DEFLATED) as zf:
        with zf.open(csv_file, "w") as raw:
            with TextIOWrapper(raw) as f:
                writer = csv.writer(f)
                writer.writerow(header)
                final = []
                indexes = []
                # TODO
                r_idx = 0
                r = country_list[r_idx]
                for v in values:
                    new_ip = fix_ip(v[0])
                    while new_ip > int(country_list[r_idx][1]):
                        r_idx += 1
                        r = country_list[r_idx]
                    if int(r[0]) <= new_ip:
                        final.append([country_list[r_idx][3]] + v)
                        writer.writerow(v + [country_list[r_idx][3]])

@click.group()
def commands():
    pass

def world():
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    world.set_index("name", drop=False, inplace=True)
    return world[world["continent"] != "Antarctica"]

@click.command()
@click.argument('zipname')
@click.argument('imgname')
def geo(zipname, imgname):
    # count occurences per country
    reader = zip_csv_iter(zipname)
    header = next(reader)
    cidx = header.index("country")
    counts = defaultdict(int)
    for row in reader:
        counts[row[cidx]] += 1

    # add color column that defaults gray, but set
    # to shade of red for higher request counts
    w = world()
    w["color"] = "0.7"

    for country, count in counts.items():
        # sometimes country names in IP dataset don't
        # match names in naturalearth_lowres -- skip those
        if not country in w.index:
            continue

        color = "lightsalmon" # >= 1
        if count >= 10:
            color = "tomato"
        if count >= 100:
            color = "red"
        if count >= 1000:
            color = "brown"
        w.at[country, "color"] = color

    ax = w.plot(color=w["color"], legend=True, figsize=(16, 4))
    ax.figure.savefig(imgname, bbox_inches="tight")
    
@click.command()
@click.argument('zipname')
@click.argument('imgname')
@click.argument('hour', type=click.INT)
def geohour(zipname, imgname, hour):
    # count occurences per country according to time
    reader = zip_csv_iter(zipname)
    header = next(reader)
    cidx = header.index("country")
    tidx = header.index("time")
    counts = defaultdict(int)
 
    for row in reader:
        if (float(row[tidx].split(':')[0]) - hour >= -1) and (float(row[tidx].split(':')[0]) - hour <= 1):
            counts[row[cidx]] += 1

    # add color column that defaults gray, but set
    # to shade of red for higher request counts
    w = world()
    w["color"] = "0.7"

    for country, count in counts.items():
        # sometimes country names in IP dataset don't
        # match names in naturalearth_lowres -- skip those
        if not country in w.index:
            continue

        color = "lightsalmon" # >= 1
        if count >= 10:
            color = "tomato"
        if count >= 100:
            color = "red"
        if count >= 1000:
            color = "brown"
        w.at[country, "color"] = color

    ax = w.plot(color=w["color"], legend=True, figsize=(16, 4))
    ax.figure.savefig(imgname, bbox_inches="tight")

@click.command()
@click.argument('zipname')
@click.argument('imgname')
def video(zipname, imgname):
    fig, ax = plt.subplots()
    for i in range(24):
        anim = FuncAnimation(fig, geohour(zipname, imgname, 24), frames=24) 
        
    anim.to_html5_video()

commands.add_command(sample)
commands.add_command(sort)
commands.add_command(country)
commands.add_command(geo)
commands.add_command(geohour)
commands.add_command(video)

if __name__ == "__main__":
    commands()
