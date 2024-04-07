Program exs18;

uses crt;

var n1: integer;

begin;

 //depois de se declarar as variaveis se apresenta ao usuario o programa.

 clrscr;
 writeln ('caro usuario este programa recebera sua idade e te dira se voce atingiu a       maioridade ou nao.');
 write ('para comecar tecle enter.');
 readkey;

 //entÆo se recebe a idade dele para definir se ele ja atingiu a maioridade ou nao.

 clrscr;
 writeln ('por favor digite sua idade.');
 readln (n1);

 clrscr;

 //entÆo se faz uma cadeia de ifs para se apresentar ao usuario se ele ja atingiu]
 //a maioridade ou nao.

 if (n1 >= 18) then
    begin
    writeln ('Voce ja atingiu a maoridade.');
    end

    else begin
         writeln ('Voce nao atingiu a maioridade.');
         end;

 writeln (' ');
 write ('para encerrar o programa precione enter.');
 readkey;

end.