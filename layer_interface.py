import layer
import menu
import get_time

class Layer_Interface:
    def __init__(self, data):
        self.data = data
        self.strat = layer.Strategy()
    
    def apply(self):
        self.strat.apply(self.data)
    
    def main_select(self):
        choice = menu.select_element("Strategy Component", ["Add filter", "Add layer", "Finish"])
        while choice != "Finish":
            if choice == "Add filter":
                self.filter_select()
            elif choice == "Add layer":
                new_layer = layer.Layer()
                self.strat.add_layer(new_layer)
            else:
                return
            self.strat.print(self.data[0]) #pass in the headers
            choice = menu.select_element("Strategy Component", ["Add filter", "Add layer", "Finish"])

    def filter_select(self):
        #select a parameter from the headers
        param = menu.select_element("Parameter", self.data[0], return_index=True)
        filter = 0
        #select a parameter
        #if the parameter is time, select tier and then span or 2 specific dates for span
        #else, just specify if it's a percentile and then the span

        if param == "DateTimes":
            filter = self.datetime_mumbojumbo()
        else:
            v_prompt = "Choose type of value"
            v_options = ["Value", "Percentile"]
            is_percentile = not menu.select_element(v_prompt, v_options, True)
            min_val = menu.select_integer("Lower bound", 0, 0)
            max_val = menu.select_integer("Upper bound", min_val, 100)
            span = layer.Span(min_val, max_val)
            if is_percentile:
                filter = layer.Perc_Filter(param, span, self.data)
            filter = layer.Val_Filter(param, span)

        self.strat.layers[-1].add_filter(filter)


    def datetime_mumbojumbo(self):
        dt_tier = menu.select_element("tier", list(layer.tier.keys()))
        if dt_tier != "Custom DateTime":
            max_val = layer.tier[dt_tier]
            start = menu.select_integer("Start " + dt_tier, 0, max_val)
            end = menu.select_integer("End " + dt_tier, start, max_val)
            return layer.Time_Filter(dt_tier, layer.Span(start, end))
        range = get_time.select_timerange()
        return layer.Time_Filter(dt_tier, layer.Span(range[0], range[1]))