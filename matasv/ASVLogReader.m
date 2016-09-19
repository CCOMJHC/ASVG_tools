function data = ASVLogReader(filename)
%% A function to read CSV logs exported using the ASV Data Export Tool
%
% Requires swallow_csv.m from http://algoholic.eu/efficient-csv-reader-for-matlab/
%
%
% Val Schmidt
% Center for Coastal and Ocean Mapping
% University of New Hamsphire
% 2016

sep = ',';
escape = '//';
quote = '"';
display(['Reading ' filename '...'])

[numbers, headers] = swallow_csv(filename,quote,sep,escape);

Nfields = size(headers,2);

for i=1:Nfields
    % Modify field names to comply with MATLAB variable naming syntax.
    fieldname = strrep(headers{1,i},' ','_');
    fieldname = strrep(fieldname,'(','_');
    fieldname = strrep(fieldname,')','');
    fieldname = strrep(fieldname,'%','Pct');
    fieldname = strrep(fieldname,'|','');
    if strcmp(fieldname(1),'1')
        fieldname = ['One' fieldname(2:end)];
    end
    % Set the field names
    data.(fieldname) = numbers(:,i);
end