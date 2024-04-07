program exs13;

uses crt;

var n1: integer;
    sal: real;

  //primeiramente se declara as variaveis.

begin;

 //depois se da um breve resumo ao usuario do que o programa ira fazer.


 clrscr;
 writeln ('caro usuario este programa lhe dara um menu de opcoes para que voce decida o que quer fazer.');
 write ('para continuar tecle enter.');
 readkey;

 // entÆo lhe mostra o menu com as op‡äes disponiveis e se le a op‡Æo que o usuario digitar para se usar na estrutura case.
 // como ‚ pedido para tratar de op‡äes que nÆo fosse as trˆs abaixo se faz um if e nele se coloca a seguinte condi‡Æo.
 // se a op‡Æo que o usuario for maior que 3 ou menor que 1 entÆo mostre a ele a mensagem op‡Æo invalida.

 clrscr;
 writeln ('escolha a opcao desejada.');
 writeln ('tecle 1 para imposto.');
 writeln ('tecle 2 para novo salario.');
 writeln ('tecle 3 para classificacao.');
 readln (n1);

 //  vantajoso colocar esta condi‡Æo aqui pois caso contrario vocˆ teria que ler o salario do usuario em todas as op‡äes do case
 // E tambem caso o usuario digite uma op‡Æo invalida j  se encerra o programa, pois ele nÆo faria nada com uma op‡Æo dessas mesmo.
 // Para se encerrar o programa se usa o comando exit que manda o ponteiro de execu‡Æo para a ultima linha do codigo.
 // E a vantagem ‚ que se esse if nÆo for atendido o programa simplesmente ir  rodar normalmente.

 clrscr;
 if (n1>3) or (n1<1) then
                      begin
                      writeln (n1,' e uma opcao invalida.');
                      writeln ('aperte qualquer tecla para encerrar o programa.');  readkey;   exit;
                      end;

 //ja que todas as op‡äes do menu envolvem salario entÆo ‚ vantajoso ler o sal rio antes de se come‡ar as estruturas.

 clrscr;
 writeln ('agora informe o seu salario.');
 readln (sal);

 clrscr;

 //aqui se come‡a a estrutura de case. e em cada op‡Æo do usuario se abre uma cadeia de ifs para realizar os comandos nescessarios.

 case n1 of

 //na primeira cadeia se impoe as condi‡äes de salario para calcular o valor do imposto.

 1:   if (sal > 850) then
         begin
         writeln (' o imposto a ser pago e de, ', sal*0.15:4:2, ' .');
         end

         else if (sal < 850) and (sal >=500) then
                 begin
                 writeln ('o imposto a ser pago e de, ', sal*0.10:4:2, ' .');
                 end

                 else if (sal < 500) then
                         begin
                         writeln ('o imposto a ser pago e de, ', sal*0.05:4:2, ' .');
                         end;


 //na segunda cadeia se impoe as condi‡äes de salario para calcular quanto ser  o novo salario.

 2:  if  (sal > 1500) then
         begin
         writeln ('o novo salario e de, ', sal+25:4:2 ,' .');
         end

         else if  (sal <= 1500) and (sal >= 750) then
                  begin
                  writeln ('o novo salario e de, ', sal+50:4:2 ,' .');
                  end

                  else if  (sal < 750) and (sal >= 450) then
                           begin
                           writeln ('o novo salario e de, ', sal+75:4:2 ,' .');
                           end

                           else if  (sal < 450) then
                           begin
                           writeln ('o novo salario e de, ', sal+100:4:2 ,' .');
                           end;

 // Na terceira como se tem somente duas op‡äes se coloca a condi‡Æo de salario que se caso nÆo for atendida,
 // So lhe resta executar o outro comando.

 3:  if (sal > 700) then
        begin
        writeln ('voce e bem remunerado.');
        end

        else
            begin
            writeln ('voce e mal remunerado.');
            end;

 end;


 writeln (' ');
 write ('para encerrar o programa precione qualquer tecla.');
 readkey;

end.
