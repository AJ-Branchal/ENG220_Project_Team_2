%% CATEGORY 2: FIREARM DEATHS AND VIOLENCE

% Age-adjusted firearm death rates per 100,000 people
% Figures are taken from the project proposal.

locations = categorical(["New Mexico", "United States"]);
locations = reordercats(locations, ...
    ["New Mexico", "United States"]);

firearmDeathRates = [26.6, 12.8];

figure;
bar(locations, firearmDeathRates);

title('Age-Adjusted Firearm Death Rates: New Mexico vs. United States (2024)');
xlabel('Location');
ylabel('Age-Adjusted Deaths per 100,000 People');

grid on;

% Add value labels above each bar.
hold on;

for i = 1:length(firearmDeathRates)
    text(i, firearmDeathRates(i), ...
        sprintf('%.1f', firearmDeathRates(i)), ...
        'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'bottom');
end

hold off;

% Year: 2024
% Sources listed in proposal: USAFacts, KFF, and Pew Research Center.
% Figures verified against KFF State Health Facts, using CDC mortality data:
% https://www.kff.org/state-health-policy-data/state-indicator/firearms-deaths-and-death-rates-per-100000/
% Rates are age-adjusted deaths per 100,000 people.
% Rates cover firearm deaths across causes, not only homicide.
