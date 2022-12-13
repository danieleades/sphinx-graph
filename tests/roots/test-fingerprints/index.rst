.. vertex:: 01

   this is a vertex directive

.. vertex:: 02
   :parents: 01:/470

   this is a vertex directive. Its parents require 'fingerprints', since this is configured as the default

.. vertex:: 03
   :type: req
   :parents: 01

   this is a vertex directive. It doesn't need 'fingerprints', since this is overridden for the 'req' type

.. vertex:: 04
   :type: req
   :require_fingerprints:
   :parents: 01:/470

   this is a vertex directive. Its parents require 'fingerprints', even though it is of the 'req' type, because this value is
   overridden on the directive itself
