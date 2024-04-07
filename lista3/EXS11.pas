program exs11;

uses crt;

var i,cont,primo,num:longint;

begin

 {Depois de se declarar as variaveis se là o numero que o usuario deseja
 verificar se Ç primo ou n∆o.}

 clrscr;

 writeln ('Digite um numero inteiro para ver se ele Ç primo ou n∆o.');
 readln (num);

 clrscr;

  {Ent∆o se cria um laáo que far† o calculo do numero dividido, por 1 ate
  o numero em quest∆o. E a cada vez que essa divis∆o for 0, o contador ira
  somar 1. Numeros primos so poderiam ter esse contador por 2, logo se este
  contador for diferente de 2 ent∆o o numero n∆o Ç primo.}

  for i:=1 to num do
      begin
      primo:= num mod i;

        if primo=0 then
           begin
           cont:=cont+1;
           end;

      end;

 {Ja sabendo-se da regra do contador so resta colocar isto em uma estrutura
 de if, considerando que o numero 1 teria como contador somente 1 ent∆o se
 adiciona ele na condiá∆o pois o numero 1 tambem Ç um numero primo.}

 if (cont=2) or (num=1) then
    begin
    writeln ('O numero ',num ,' Ç um numero primo.');
    end

    else begin
         writeln ('O numero ',num ,' n∆o Ç um numero primo.');
         end;

 writeln;
 write ('Para encerrar o programa pressione qualquer tecla.');
 readkey;

end.