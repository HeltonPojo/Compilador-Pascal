program exs15;

uses crt;

var preco,maior,menor,total_imp,imposto,fim,adicional: real;
    i,qtd_barato,qtd_normal,qtd_caro,custo_est:integer;
    refri,cat: char;

    //aqui se declara as variaveis.


begin

 clrscr;

 maior:=0;
 menor:=30000;

 for i:=1 to 12 do
     begin
     //e aqui se le os dados do produto que o usuario digitar†.

     clrscr;
     writeln ('Digite o preáo do produto.');
     readln (preco);
     writeln ('Digite S se o produto necessitar de refrigeraá∆o.');
     writeln ('Digite N se o produto n∆o necessitar de refrigeraá∆o.');
     readln (refri);
     writeln ('Digite a categoria do produto.');
     writeln ('A para alimentaá∆o.');
     writeln ('L para limpeza.');
     writeln ('V para vestuario.');
     readln (cat);

     {Abaixo nas varias cadeias de ifs sera feita a definiá∆o de quanto sera o
     custo de estocagem.}

     if (preco <20) then
        begin

        if (cat='A') then
           begin
           custo_est:=2;
           end

           else if (cat='L') then
                   begin
                   custo_est:=3;
                   end

                   else if (cat='V') then
                           begin
                           custo_est:=4;
                           end


        end;

     if (preco >= 20) and (preco <=50) then
        begin
           if (refri='S') then
              begin
              custo_est:=6;
              end

              else if refri='N' then
                      begin
                      custo_est:=0;
                      end
        end;


     if (preco >50) then
        begin
           if (refri='S') then
              begin
              if (cat='A') then
                 begin
                 custo_est:=5;
                 end

                 else if (cat= 'L') then
                         begin
                         custo_est:=2;
                         end

                         else if (cat='V') then
                                 begin
                                 custo_est:=4;
                                 end
              end

              else if  (refri='N') then
                       begin
                         if (cat='A') or (cat='V') then
                            begin
                            custo_est:=0;
                            end

                            else if (cat='L') then
                                    begin
                                    custo_est:=1;
                                    end
                       end


        end;

        //se define o imposto.

        if (cat='A') or (refri='S') then
           begin
           imposto:=preco*0.04;
           end

           else begin
                imposto:=preco*0.02;
                end;


       fim:=preco+imposto+custo_est;

       //aqui se apresenta os resultados do produto singular.

       writeln ('O custo de estocagem Ç de, R$',custo_est,' .');
       writeln ('O imposto Ç de, R$',imposto:0:2,' .');
       writeln ('O preáo final Ç de, R$',fim:0:2,' .');

       {Se define a classificaá∆o do produto e se faz a contagem para no
       final se apresentar quantos de cada classificaá∆o tem produtos.}

       if (fim<20) then
          begin
          writeln ('A classificaá∆o do produto Ç barato.');
          qtd_barato:=qtd_barato+1;
          end

          else if (fim>=20) and (fim<=100) then
                  begin
                  writeln ('A classificaá∆o do produto Ç medio.');
                  qtd_normal:=qtd_normal+1;
                  end

                  else if (fim>100) then
                          begin
                          writeln ('A classficaá∆o do produto Ç caro.');
                          qtd_caro:=qtd_caro+1;
                          end;

       {Se calcula o adicional total e o imposto total, e logo em seguida
       se define qual o maior preáo e qual o menor preáo.}

       adicional:=adicional+imposto+custo_est;
       total_imp:=total_imp+imposto;

       if (maior < preco) then
          begin
          maior:=preco;
          end;

       if (menor < preco) then
          begin
          menor:=preco;
          end;



     end;

  //se apresenta os resultados finais ao usuario.

  writeln ('O maior preáo Ç de, R$',maior:0:2,' .');
  writeln ('O menor preáo Ç de, R$',menor:0:2,' .');
  writeln ('A media dos valores adicionais Ç de, R$',adicional:0:2,' .');
  writeln ('O total dos impostos Ç de, R$',total_imp:0:2,' .');
  writeln ('A quantidade de produtos com classificaá∆o barato Ç de, ',qtd_barato,' .');
  writeln ('A quantidade de produtos com classificaá∆o medio Ç de, ',qtd_normal,' .');
  writeln ('A quantidade de produtos com classificaá∆o caro Ç de, ',qtd_caro,' .');
  writeln;
  write ('Para encerrar o programa pressione qualquer tecla.');
  readkey;

end.