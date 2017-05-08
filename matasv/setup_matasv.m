%% A script to setup the matasv toolbox. 
%
% Val Schmidt
% Center for Coastal and Ocean Mapping
% University of New Hamsphire

setupfile = mfilename('fullpath');
[matasvdir ~] = fileparts(setupfile);

% An anonymous function to check to see if a directory is already in the
% path.
isInPath = @(direct) sum(strcmp(strsplit(path(),pathsep),direct));

if isInPath(matasvdir)==0
    addpath(matasvdir)
end

