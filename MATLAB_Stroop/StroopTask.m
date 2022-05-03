function StroopTask(name,num)

% Takes 2 variables, 'name' of participant, and number of tasks, and outputs
% a file with the structure nameMMDDHHMM.csv

congtime = zeros(1,num);        % Creates empty variables/arrays to be used
incongtime = zeros(1,num);      % later
numwrong = 0;
lastrand = [];

color = {'red    ', 'green  ', 'blue   ', 'magenta'};

%% create and open empty figure with instructions

box = figure();
set(box, 'NumberTitle', 'off', ...
       'Name', 'Stroop Test', ...
       'Color', 'white', ...
       'MenuBar','none', ...
       'ToolBar', 'none');
inst = annotation('textbox', [0.1, 0.1, 0.8, 0.8], 'String',...
    "You will be shown words, one at a time, with different color backgrounds." + ...
    " Press R for words printed on red, G for green, B for blue and M for" + ...
    " magenta. Try to be as fast as possible but correct. Now press enter" + ...
    " to start the experiment",'FontSize',20);

w = waitforbuttonpress();       % This is where participant presses enter to continue
delete(inst);                   % Deletes the instructions

%% Beginning of actual stroop task. Each task is an interation of the For Loop,
%   using the num input as total number of tasks. For each task a random number
%   is used to define the background color and the text displayed, ensuring
%   no background colors are sequentially repeated.

for i = 1:num
    rand1 = randi(4);
    rand2 = randi(4);
    while i ~= 1 & rand2 == lastrand2 
        rand2 = randi(4);
    end
    uicontrol('Style','text', 'String', color{rand1},...    % uicontrol simply displays the text and background color
        'BackgroundColor', color{rand2},...
        'Position',[300 400 200 60],...
        'ForegroundColor', 'black',...
        'FontSize', randi(20)+15);

    lastrand2 = rand2;          % used to save previous background into next iteration

    time1 = datetime;           % tracks response time
    w = waitforbuttonpress;
    time2 = datetime;
 
%% Tracks participants response as an ASCII value and converted back to color choice

    value = double(get(gcf,'CurrentCharacter'));

    if value == 114
        choice = 'red    ';
    elseif value == 103
        choice = 'green  ';
    elseif value == 98
        choice = 'blue   ';
    elseif value == 109
        choice = 'magenta';
    end

    if choice == color{rand2}       % determines if participant's response is correct AND if the word and background color displayed were congruent
        disp('correct')
        if rand1 == rand2
            congtime(i) = seconds(time2 - time1);
        else
            incongtime(i) = seconds(time2 - time1);
        end
    else
        disp('wrong')
        numwrong = numwrong + 1     % tracks the number of participant's incorrect responses
    end

end

close all 

%% After figure closes, combines recorded times for each response into usable data for analysis, and creates output file

congtime(congtime == 0) = NaN;          % congtime = response time for congruent color tasks
incongtime(incongtime == 0) = NaN;      % incongtime = response time for incongruent color tasks
congavg = mean(congtime,'omitnan');
incongavg = mean(incongtime,'omitnan');
congsd = std(congtime, 'omitnan');
incongsd = std(incongtime, 'omitnan');

outputinfo = [congavg, congsd, incongavg, incongsd, numwrong, num];
outputfile = array2table(outputinfo);
outputfile.Properties.VariableNames(1:6) = {'congruent_avg',...
    'congruent_stdev','incongruent_avg','incongruent_stdev',...
    'number_wrong','total_number'};
outputname = strcat(name,datestr(now,'mmddHHMM'),'.csv');
writetable(outputfile,outputname);

end