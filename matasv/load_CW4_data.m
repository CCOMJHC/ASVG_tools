function [pos, vtg, rmc, att, hdg, engine, pilot, vehiclestate, vehicle] = load_CW4_data(directory)
%% A function to load all parsed data from a CW4 extracted_logs directory.
%
% [pos, vtg, rmc, att, hdg,...
%   engine, pilot, vehiclestate, vehicle] = load_CW4_data([directory])
%
% 
if isempty(directory)
   directory = uigetdir(); 
end

[pathstr, dirstr, suf] = fileparts(directory);

disp('Loading GGA')
    
if exist([directory filesep 'GGA.txt'],'file')
    pos = load([directory filesep 'GGA.txt']);
elseif exist([directory filesep 'GGA_3_.txt'],'file')
    pos = load([directory filesep 'GGA_3_.txt']);
else
    disp('Unable to find GGA.txt')
    pos = [];
end
disp('Loading VTG')
if exist([directory filesep 'VTG.txt'],'file')
    vtg = load([directory filesep 'VTG.txt']);
elseif exist([directory filesep 'VTG_3_.txt'],'file')
    vtg = load([directory filesep 'VTG_3_.txt']);
else
    disp('Unable to find VTG.txt')
    vtg = [];
end
disp('loading RMC')
if exist([directory filesep 'RMC.txt'],'file')
    rmc = load([directory filesep 'RMC.txt']);
elseif exist([directory filesep 'RMC_3_.txt'],'file')
    rmc = load([directory filesep 'RMC_3_.txt'],'file');
else
    disp('Unable to find RMC.txt')
    rmc = [];
end

if exist([directory filesep 'nmea2000_attitude_pgn127257.mat'],'file')
    disp('Loading attitude')
    load([directory filesep 'nmea2000_attitude_pgn127257.mat'])
else
    try
        disp('Parsing attitude')
        att = import_nmea2000_attitude([directory filesep 'nmea2000_attitude_pgn127257.txt']);
        save([directory filesep 'nmea2000_attitude_pgn127257.mat'],'att')
    catch
        disp('Unload to load or parse attitude.')
        att = [];
    end
end
if exist([directory filesep 'nmea2000_vessel_heading_pgn127250.mat'],'file')
    disp('Loading heading')
    load([directory filesep 'nmea2000_vessel_heading_pgn127250.mat'])
else
    try
        disp('Parsing hdg')
        hdg = import_nmea2000_heading([directory filesep 'nmea2000_vessel_heading_pgn127250.txt']);
        save([directory filesep 'nmea2000_vessel_heading_pgn127250.mat'],'hdg')
    catch
        disp('Unable to load or parse heading.')
        hdg = [];
    end
end
% Need error checking for these too. 
load([directory filesep 'engine.mat'])
load([directory filesep 'pilot.mat'])
load([directory filesep 'vehiclestate.mat'])
load([directory filesep 'vehicle.mat'])

