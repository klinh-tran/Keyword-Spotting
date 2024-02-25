close all
clc
clear all

rootin = 'audio\';
A = dir([rootin '*.wav']);
rootout = 'sample\';
%mkdir(rootout)

neg = 10;
for n=1:neg
    m = floor(rand(1,1)*length(A))+1;
    fname = A(m).name;
    copyfile([rootin fname],[rootout fname]);
end
    