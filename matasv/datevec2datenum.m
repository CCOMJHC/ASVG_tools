function dts = datevec2datenum(d)
%% A function to convert a matrix having columes of YYYY MM DD HH MM SS into MATLAB serial format.

dts = datenum(d(:,1),d(:,2),d(:,3),d(:,4),d(:,5),d(:,6));

