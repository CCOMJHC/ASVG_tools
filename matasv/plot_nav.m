function plot_nav(directory,plotdir)
%% A function to plot nav data from CW4

if isempty(directory)
    directory = uigetdir();
end
[pathstr, dirstr, suf] = fileparts(directory);

if isempty(plotdir)
    plotdir='.';
end

defaultfontsize = get(0,'DefaultAxesFontSize');
set(0,'DefaultAxesFontSize',10)

[pos, vtg, rmc, att, hdg, engine, pilot, vehiclestate, vehicle] = ...
    load_CW4_data(directory);


%%
pos_logtime = datevec2datenum(pos(:,1:6));
pos_gpstime = datevec2datenum(pos(:,7:12));
vtg_logtime = datevec2datenum(vtg(:,1:6));
att_time = unixtime2mat(att.log_timestamp);
hdg_time = unixtime2mat(hdg.log_timestamp);
eng_time = unixtime2mat(engine.Epoch_Time_s);
pilot_time = unixtime2mat(pilot.Epoch_Time_s);
vs_time = unixtime2mat(vehiclestate.Epoch_Time_s);


%%
lat = pos(:,13);
lon = pos(:,14);
[e n z] = deg2utm(lat,lon);
distanceTraveled = cumsum(sqrt(diff(e).^2 + diff(n).^2));
addpath ~/math/matlab/subtightplot/subtightplot/
%%
figure
set(gcf,'Position',[466         135        1079         709])
axisgap = .07;

subtightplot(6,4,[1 2 9 10],[axisgap axisgap],[.01 .01],[.07 .01]);
plot(lon,lat,'y')
plot_google_map('maptype','satellite')
title(directory)

H(1) = subtightplot(6,4,[13 14],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(att_time,att.roll*180/pi,'linewidth',2);
hold on
vplot(att_time,att.pitch*180/pi,'linewidth',2);
hold off
ylabel('roll/pitch','fontsize',10)
dynamicDateTicks()

H(2) = subtightplot(6,4,[17 18],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(vtg_logtime,vtg(:,8),'linewidth',2)
ylabel('smg,kts','fontsize',10)
dynamicDateTicks()
% FIX: heading is not corrected for magenetic variation. Needs to be added
% when RMC string is properly parsed. (it's not currnetly included).
H(3) = subtightplot(6,4,[21 22],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(hdg_time,hdg.heading_sensor_reading*180/pi,'linewidth',2);
hold on
vplot(vtg_logtime,vtg(:,7),'linewidth',2)
hold off
ylabel('heading/cmg','fontsize',10)
dynamicDateTicks()





H(4) = subtightplot(6,4,[3 4],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(eng_time,engine.Primary_Fuel_Level_Pct,'.')
hold on
vplot(eng_time,engine.Secondary_Fuel_Level_Pct,'.')
hold off
ylabel('fuel 1/2','fontsize',10)
dynamicDateTicks()

H(5) = subtightplot(6,4,[7 8],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(eng_time,engine.Eng_Speed_rpm,'.')
ylabel('rpm','fontsize',10)
dynamicDateTicks()

H(6) = subtightplot(6,4,[11 12],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(eng_time,engine.Coolant_Temp_deg_C,'.')
ylabel('cool temp','fontsize',10)
dynamicDateTicks()

H(7) = subtightplot(6,4,[15 16],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(eng_time,engine.Oil_Pressure_kPa,'.')
ylabel('oil kPa','fontsize',10)
dynamicDateTicks()

H(8) = subtightplot(6,4,[19 20],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(eng_time,engine.Alternator_Current_A,'.')
ylabel('alt amps','fontsize',10)
dynamicDateTicks()

H(8) = subtightplot(6,4,[23 24],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(vs_time,vehiclestate.Vehicle_State,'o')
ylabel('veh state','fontsize',10)
dynamicDateTicks()

linkaxes(H,'x')
savefig(gcf,[plotdir filesep dirstr '_plot1'],'compact')
print([plotdir filesep dirstr '_plot1'],'-dpng')
%%
figure
set(gcf,'Position',[466         135        1079         709])

subtightplot(6,4,[1 2 9 10],[axisgap axisgap],[.01 .01],[.07 .01]);
plot(lon,lat,'y')
plot_google_map('maptype','satellite')

HH(1) = subtightplot(6,4,[13 14],[axisgap axisgap],[.01 .01],[.07 .01]);
[LL, L1, L2] = plotyy(pilot_time,pilot.DrvTrn_Cmded_Eng_Throttle_Pct,vtg_logtime,vtg(:,8),'stem','plot');
ylabel(LL(1),'cmd eng throttle','fontsize',10)
ylabel(LL(2),'sog, kts','fontsize',10)
dynamicDateTicks
grid minor

HH(2) = subtightplot(6,4,[17 18],[axisgap axisgap],[.01 .01],[.07 .01]);
[LL2, L3, L4] = plotyy(pilot_time,pilot.DrvTrn_Cmded_Deflector_Pos_Pct,...
    pilot_time, pilot.DrvTrn_Meas_Deflector_Pos_Pct);
ylabel(LL2(1),'cmd deflector','fontsize',10)
ylabel(LL2(2),'meas deflector','fontsize',10)
set(L3,'linestyle','none','marker','.')
set(L4,'linestyle','none','marker','.')
dynamicDateTicks
grid minor

HH(3) = subtightplot(6,4,[21 22],[axisgap axisgap],[.01 .01],[.07 .01]);
[LL3, L5, L6] = plotyy(pilot_time,pilot.DrvTrn_Cmded_Jet_Steerage_Pct,...
    pilot_time, pilot.DrvTrn_Meas_Jet_Steerage_Pct);
ylabel(LL3(1),'cmd steerage','fontsize',10)
ylabel(LL3(2),'meas steerage','fontsize',10)
set(L5,'linestyle','none','marker','.')
set(L6,'linestyle','none','marker','.')
dynamicDateTicks
grid minor

HH(4) = subtightplot(6,4,[3 4],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(pilot_time,pilot.DrvTrn_Deflector_Pos_Eff_Pct,'.')
ylabel('effort %','fontsize',10)
set(gca,'fontsize',12)
dynamicDateTicks

HH(5) = subtightplot(6,4,[7 8],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(pilot_time,pilot.HeadingCtl_Kp,'.r')
hold on
vplot(pilot_time,pilot.HeadingCtl_Ki,'.g')
vplot(pilot_time,pilot.HeadingCtl_Kd,'.')
hold off
set(gca,'fontsize',12)
ylabel('hdg pid (RGB)','fontsize',10)
dynamicDateTicks

HH(6) = subtightplot(6,4,[11 12],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(pilot_time,pilot.SpeedCtl_Kp,'.r')
hold on
vplot(pilot_time,pilot.SpeedCtl_Kd,'.')
hold off
ylabel('spd pd (RB)','fontsize',10)

dynamicDateTicks

HH(6) = subtightplot(6,4,[15 16],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(pilot_time,pilot.Status,'o')
set(gca,'fontsize',12)
ylabel('status','fontsize',10)
dynamicDateTicks

HH(7) = subtightplot(6,4,[19 20],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(pilot_time,pilot.SpeedCtl_SpeedCtl_Error_kts,'.')
set(gca,'fontsize',12)
ylabel('spd ctrl error','fontsize',10)
dynamicDateTicks

HH(8) = subtightplot(6,4,[23 24],[axisgap axisgap],[.01 .01],[.07 .01]);
vplot(pilot_time,pilot.HeadingCtl_HeadingCtl_Error_deg,'.')
set(gca,'fontsize',12)
ylabel('hdg ctrl error','fontsize',10)
dynamicDateTicks

linkaxes(HH,'x')
try
    savefig(gcf,[plotdir filesep dirstr '_plot2'],'compact')
catch
    disp('Failed to save fig. Data size may be too big.')
end
print([plotdir filesep dirstr '_plot2'],'-dpng')
%%
set(0,'DefaultAxesFontSize',defaultfontsize)