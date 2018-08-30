function out = openph5(filename)
%% A function to read pandas HDF5 files in table format (Drag and Drop)
%
% Val Schmidt
% CCOM/JHC
% 2018

data = read_pandas_h5(filename );

if nargout==1
   out = data;
else
   assignin('base',data.name,data);
end

