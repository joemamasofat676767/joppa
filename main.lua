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

local modules = require("modules")

local knowledge = modules.GoodMap()

print(knowledge)

knowledge:GoodMap_add({1,2,3}, {4,5,6})
knowledge:GoodMap_remove({1,2,3})
knowledge:GoodMap_add({7,8,9}, {10,11,12})
print(knowledge:GoodMap_get({7,8,9})[1])
local obama = modules.parse()
print(obama:GoodMap_get({9,10,11,12,13,14,15,16,17,18})[4])

print(modules.math_CosineSim({1,2,3}, {4,5,6}))

local function LoadBar(amount, length)
	length = length or 50
	return coroutine.wrap(function()
		local bar_point = length / amount
		local bar = 0
		while amount > 0 do
			amount = amount - 1
			bar = bar + bar_point
			io.write(
				string.rep("\b", length+15) ..
				string.rep("█", math.floor(bar)) ..
				string.rep(" ", length-math.floor(bar)) ..
				string.format(" %6.2f%%", bar/length*100)
			)
			io.flush()
			coroutine.yield(nil)
		end
	end)
end

local bar = LoadBar(100, 100)
for _ = 1, 100 do
	bar()
end
print()
