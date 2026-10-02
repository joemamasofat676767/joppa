--[[
def LoadBar(amount, length=50):
	bar_point = length / amount
	bar = 0
	while amount > 0:
		amount -= 1
		bar += bar_point
		print("\b"*(length+14),
			"█"*floor(bar),
			" "*(length-floor(bar)),
			f"{bar/length*100:6.2f}%",
			end="", flush=True)
		yield ...
]]

package.cpath = "./?.so;" .. package.cpath

local heavy = require("heavy")

heavy.hello()

local function LoadBar(amount, length)
	length = length or 50
	return coroutine.wrap(function()
		local bar_point = length / amount
		local bar = 0
		while amount > 0 do
			amount = amount - 1
			bar = bar + bar_point
			io.write(
				string.rep("\b", length+14) ..
				string.rep("█", math.floor(bar)) ..
				string.rep(" ", length-math.floor(bar)) ..
				string.format("%6.2f%%", bar/length*100)
			)
			io.flush()
			coroutine.yield(nil)
		end
	end)
end

local bar = LoadBar(100)
for _ = 1, 100 do
	bar()
end
