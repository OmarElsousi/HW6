#region class definitions
class VoltageSource():
    #region constructor
    def __init__(self, V=12.0, name='ab'):
        """
        Define a voltage source in terms of self.Voltage = V, self.Name = name
        :param V: The voltage
        :param name: the name of voltage source
        """
        #region attributes
        self.Voltage = V
        self.Name = name
        # Optionally store 'Type' if you wish
        self.Type = "DC"  # default or set as needed
        #endregion
    #endregion
#endregion
