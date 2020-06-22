# Clean the station-inventory CSV file of unnecessary information to reduce its size
# Then, put the data into docs/index.html in the station select dropdown.
import pandas, argparse, os, time, math

path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="Tool to strip unnecessary data from the Environment Canada station inventory")
parser.add_argument("--csv", default=f"{path}/Station Inventory EN.csv",)
args = parser.parse_args()

data = pandas.read_csv(args.csv, skiprows = 3)

# Map values of x (for which x E [x < 1]u[12 < x]) into a valid month
# Combine sawtooth function with greatest-integer to create a period of 12 for which 0 = 12, 1 = 1, ..., 11 = 11, 12 = 12
def valid_month(x):
	g_int = lambda x: math.ceil(x)
	saw = lambda x: x - math.floor(x)
	valid = 12*(saw(1/12 * g_int(x-1)))+1
	return str(int(valid)).rjust(2, '0')

local = time.localtime()
m2 = valid_month(local.tm_mon - 6)
y2 = local.tm_year if int(m2) < local.tm_mon else local.tm_year - 1
delta = {
	"min": y2,
	"max": local.tm_year
}

slim = data.loc[data["First Year"] <= delta["min"]]
slim = slim.loc[slim["Last Year"] >= delta["max"]]
slim = slim[["Name", "Province", "Station ID"]]
slim.to_json(f"{path}/station-inventory.json", orient="records")
