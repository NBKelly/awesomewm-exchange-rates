local awful = require("awful")
local beautiful = require("beautiful")
local wibox = require("wibox")

--local function myPopup(prices)
--  local popup = awful.popup {
--    ontop = true,
--    visible - false, --should be hidden when created
--    shape = function(cr, width, height)
--      gears.shape.rounded_rect(cr, width, height, 4)
--  }
--end

function rateWidget()
  local function setPrices(widget)
    widget:set_text(widget.prices[widget.price_index])
  end

  mywidget = wibox.widget {
    widget = wibox.widget.textbox,
    valign = "center",
    halign = "center",
    markup = "??",
    margins = 4,
    spacing = 4,
    price_index = 1,
    prices = {},
    --set_price = function(self) self:set_text(self.prices[self.price_index]) end
    --buttons = {
    --  awful.button({}, 1, nil, function ()
    --    local popup = awful.popup()
    --    print("Mouse was clicked")
    --  end)
    --}
  }

  mywidget = awful.widget.watch('bash -c "python3 ~/.config/awesome/rateWidget/rates.py"', 3600,
  	                        function(widget, stdout)
				  local lines = {}
				  for s in stdout:gmatch("[^\r\n]+") do
				    table.insert(lines, s)
				  end
				  widget.prices = lines
				  if(widget.price_index > #lines) then
				    widget.price_index = 1
				  end
				  
				  setPrices(widget)
				  
				  return
				end,
				mywidget)

  -- on click
  mywidget:connect_signal('button::press', function(c)
    c.price_index = 1 + (c.price_index % #c.prices)
    setPrices(c)
  end)
  
  return mywidget
end

