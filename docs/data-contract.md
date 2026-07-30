# Data contract

Reaction networks use schemas/reaction-network.schema.json. Experimental and spectroscopy metadata use schemas/experiment.schema.json. CSV column names, quantities, units, species mapping, preprocessing, acquisition conditions, and calibration roles must be declared. Original uploaded data are immutable. Derived data must record source file, transform, software version, timestamp, and split. Spectroscopy signals require a separately validated calibration model before they are treated as concentration measurements.
