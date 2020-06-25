# Clean the station-inventory CSV file of unnecessary information to reduce its size
# Then, put the data into docs/index.html in the station select dropdown.
import pandas, argparse, os, time

path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="Tool to strip unnecessary data from the Environment Canada station inventory")
parser.add_argument("--csv", default=f"{path}/Station Inventory EN.csv",)
args = parser.parse_args()

data = pandas.read_csv(args.csv, skiprows = 3)

local = time.localtime()
past = local.tm_year if local.tm_mon > 6 else local.tm_year - 1
delta = [local.tm_year, past]

slim = data.loc[data["First Year"] <= min(delta)]
slim = slim.loc[slim["Last Year"] >= max(delta)]
slim = slim[["Name", "Province", "Station ID"]]
slim.to_json(f"{path}/station-inventory.json", orient="records")
