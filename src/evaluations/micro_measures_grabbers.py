
class MicroMeasuresGrabber:

    def measures_to_capture(self):
        return ['interactions','mouseTraceLength','mouseDwellTime','hoverAndBack','exitAndBack']

    def is_log_valid(self, widget_log):
        return widget_log['interactions'] > 0
    
    def get_measures_for_prediction(self, widget_log):
        return [widget_log[measure_name] for measure_name in self.measures_ordered()]

class TextInputGrabber(MicroMeasuresGrabber):

    def measures_to_capture(self):
        return super().measures_to_capture() + ['typingLatency','focusTime','typingSpeed','typingVariance','correctionAmount','inputSwitches','enteredText']
    
    def measures_ordered(self):
        return ['correctionAmount', 'focusTime', 'inputSwitches', 'interactions', 'mouseDwellTime','mouseTraceLength','typingLatency','typingSpeed','typingVariance']

class SelectInputGrabber(MicroMeasuresGrabber):
    
    def measures_to_capture(self):
        return super().measures_to_capture() + ['optionsSelected','optionsDisplayTime','optionsCount']
    
    def measures_ordered(self):
        return ['interactions','mouseDwellTime','mouseTraceLength','optionsDisplayTime', 'optionsSelected']

class AnchorGrabber(MicroMeasuresGrabber):
    
    def measures_to_capture(self):
        return super().measures_to_capture() + ['misclicks']

    def measures_ordered(self):
        return ['interactions','mouseDwellTime','mouseTraceLength']
    
class DatepickerGrabber(MicroMeasuresGrabber):
    
    def measures_to_capture(self):
        return super().measures_to_capture() + ['selections', 'clicks']
    
    def measures_ordered(self):
        return ['clicks','interactions','mouseDwellTime','mouseTraceLength','selections']

class RadiosetGrabber(MicroMeasuresGrabber):

    def is_log_valid(self, widget_log):
        return widget_log['selections'] > 0
    
    def measures_to_capture(self):
        return super().measures_to_capture() + ['hoverToFirstSelection', 'clicks', 'selections', 'optionsCount']
    
    def measures_ordered(self):
        return ['clicks','hoverToFirstSelection', 'interactions','mouseDwellTime','mouseTraceLength','selections']

grabbers = {
    'TextInput': TextInputGrabber(),
    'SelectInput': SelectInputGrabber(),
    'RadioSet': RadiosetGrabber(),
    'Anchor': AnchorGrabber(),
    'Datepicker': DatepickerGrabber(),
    'DateSelect': SelectInputGrabber()
}