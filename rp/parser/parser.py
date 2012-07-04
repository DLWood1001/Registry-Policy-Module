
class Parser(object):
    def __init__(self):
        self.file_handle    = None
        self.states         = dict()
        self.memory         = dict()

    def add_state(self, state_name, state):
        self.states[state_name] = state
    
    def add_states(self, **states):
        for state_name, state_value in states.iteritems():
            self.add_state(state_name, state_value)

    def parse(self, file_name, initial_state, initial_memory):
        self.file_handle = open(file_name, 'rb')
        self.memory = initial_memory
        
        next_state = initial_state
        
        while (True):
            state = self.states[next_state](self.memory)
            
            data_size = state.data_size
            
            if data_size > 0:
                while (True):
                
                    data = self.file_handle.read(data_size)
                
                    if not data:
                        return True
                
                    if (state.process(data)):
                        break
            
            next_state = state.next_state
            
            if next_state == None:
                return True
            

class State(object):
    def __init__(self, memory):
        raise NotImplementedError()
    
    def process(self, data):
        raise NotImplementedError()
    

    



    
