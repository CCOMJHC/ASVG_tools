function plot_engine(engine,varargin)
%% A function to plot engine data

if length(varargin) == 1
    vehicle = varargin{1};
end

fieldnames = fields(engine);
Nplots = length(fieldnames) - 1;

matengtime = unixtime2mat(engine.(fieldnames{1}));
maxRows = 5;
cols = floor(Nplots./maxRows);
if cols == 0
    cols = 1;
    rows = Nplots;
else
    rows = maxRows;
end

if mod(Nplots,maxRows) > 0
    cols = cols+1;
end
H = tight_subplot(rows,cols,[.03 .05],[.1,.01],[.01 .01]);
for i=1:Nplots
    z = i+1;
    %    H(i) = subplot(Nplots,cols,i);
    axes(H(i))
    plot(matengtime,engine.(fieldnames{z}),...
        '.-',...
        'linewidth',3)
    grid on
    if i < Nplots
        set(gca,'Xtick',[])
        
    else
        xlabel('Time')
        datetick('x')
    end
    
    title(fieldnames{z},...
        'FontSize',8)
    
    linkaxes(H,'x')
end
        





