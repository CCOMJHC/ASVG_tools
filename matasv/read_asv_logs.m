function read_asv_logs(indirectory,varargin)
%% A function to read and parse a directory of ASV logs.
%
% Usage:
%  read_asv_logs('/path/to/csv/file/directory',['/optional/path/to/output/directory'])
%
% Val Schmidt
% Center for Coastal and Ocean Mapping
% University of New Hampshire
% 20106

if ~isempty(varargin)
    outputdir = varargin{1};
else
    outputdir = indirectory;
end

if ~exist(indirectory,'dir')
    error('No such input directory');
end

apo = char(39);

% Get the names of the csv files in the directory
files = dir([indirectory filesep '*']);

% Loop throught the files.
for i=1:length(files)
    if length(files(i).name) < 4
        continue  % Skips '.' and '..'
    elseif strcmp(files(i).name(end-3:end),'.csv')
        datasetname = files(i).name(1:end-4);  % Capture the file name to use as the data set name
        eval([datasetname '= ASVLogReader(' apo indirectory filesep files(i).name apo ');'])
        
        save([ outputdir datasetname '.mat'],datasetname)
    else
        continue
    end
    
    
end

