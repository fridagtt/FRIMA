
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programaARROW ASSIGN COLON COMMA CTECHAR CTEF CTEI CTESTRING DECIMAL DESDE DIVIDE ENTERO EQUAL FUNCION GREATER GREATEREQ HASTA ID IMPRIMIR INICIO LBRACE LBRACKET LEER LESS LESSEQ LETRA LPAREN MIENTRAS MINUS NOTEQUAL O PLUS PROGRAMA RBRACE RBRACKET REGRESAR RENGLON RPAREN SEMICOLON SI SINO SINREGRESAR TABLA TIMES VARIABLE Y\n  programa : PROGRAMA ID punto_programa COLON inicio\n          | PROGRAMA ID punto_programa COLON dec_var_cycle inicio\n          | PROGRAMA ID punto_programa COLON dec_var_cycle dec_func_cycle inicio\n          | PROGRAMA ID punto_programa COLON dec_func_cycle inicio\n  \n  punto_programa : \n  \n  inicio : INICIO LPAREN RPAREN LBRACE punto_update_goto inicio_estatutos RBRACE SEMICOLON\n  \n  inicio_estatutos : estatutos_opciones inicio_estatutos\n                    | empty\n  \n  punto_update_goto :\n  \n  dec_var_cycle : dec_var dec_var_cycle\n                | empty\n  \n  dec_func_cycle : dec_func p_dec_func_aux\n  \n  p_dec_func_aux : dec_func p_dec_func_aux\n                  | empty\n  \n  dec_var : simple_var\n          | array\n          | matrix\n  \n  type : ENTERO\n      | DECIMAL\n      | LETRA\n  \n  simple_var : VARIABLE type ARROW ID punto_simple_var simpleVarCycle SEMICOLON\n  simpleVarCycle : COMMA ID punto_simple_var simpleVarCycle\n                  | empty\n  \n  punto_simple_var :\n  \n  array : RENGLON type ARROW ID LBRACKET CTEI RBRACKET punto_array arrayCycle SEMICOLON\n  arrayCycle : COMMA ID LBRACKET CTEI RBRACKET punto_array arrayCycle\n              | empty\n  \n  punto_array :\n  \n  matrix : TABLA type ARROW ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET punto_matrix matrixCycle SEMICOLON\n  matrixCycle : COMMA ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET punto_matrix matrixCycle\n              | empty\n  \n  punto_matrix :\n  \n  dec_func : FUNCION type ID punto_add_func punto_global_func_var LPAREN parameter RPAREN LBRACE dec_var_cycle estatutos RBRACE SEMICOLON punto_end_function\n            | FUNCION SINREGRESAR ID punto_add_func LPAREN parameter RPAREN LBRACE dec_var_cycle estatutos RBRACE SEMICOLON punto_end_function\n  \n  punto_global_func_var : \n  \n  punto_end_function :\n  \n    punto_add_func :\n    \n  parameter : type ID punto_add_parameter parameterCycle\n            | empty\n  \n  parameterCycle : COMMA type ID punto_add_parameter parameterCycle\n                  | empty \n  \n  punto_add_parameter :\n  \n  estatutos : estatutosCycle\n            | func_regresar\n  \n\testatutosCycle : estatutos_opciones estatutos\n                | estatutos_opciones\n\t\n  estatutos_opciones : asignar\n                      | llamada_func_void\n                      | ciclo_for\n                      | ciclo_while\n                      | condicion\n                      | imprimir\n                      | leer\n  \n  func_regresar : REGRESAR exp SEMICOLON punto_check_types\n  \n  punto_check_types :\n  \n  asignar : variable ASSIGN push_op_igual hyper_exp check_op_igual SEMICOLON\n  \n  variable : ID variable_aux\n  \n  variable_aux : LBRACKET exp RBRACKET\n              | LBRACKET exp RBRACKET LBRACKET exp RBRACKET\n              | punto_push_id\n  \n  punto_push_id : \n  \n  push_op_igual :\n  \n  check_op_igual :\n  \n  leer : LEER LPAREN punto_push_leer ID punto_create_leer RPAREN SEMICOLON\n  \n  punto_push_leer :\n  \n  punto_create_leer :\n  \n  ciclo_while : MIENTRAS punto_inicio_while LPAREN hyper_exp RPAREN punto_medio_while LBRACE estatutos RBRACE punto_fin_while SEMICOLON\n  \n  punto_inicio_while :\n  \n  punto_medio_while :\n  \n  punto_fin_while :\n  \n  ciclo_for : DESDE LPAREN ID punto_existe_id ASSIGN hyper_exp RPAREN punto_valida_int HASTA  LPAREN hyper_exp RPAREN punto_valida_exp LBRACE estatutos RBRACE punto_termina_for SEMICOLON\n  \n  punto_existe_id : \n  \n  punto_valida_int : \n  \n  punto_valida_exp : \n  \n  punto_termina_for : \n  \n  condicion : SI LPAREN hyper_exp RPAREN punto_si LBRACE estatutos RBRACE punto_fin_si SEMICOLON\n            | SI LPAREN hyper_exp RPAREN punto_si LBRACE estatutos RBRACE SINO punto_sino LBRACE estatutos RBRACE punto_fin_si SEMICOLON\n  \n  punto_si : \n  \n  punto_fin_si :\n  \n  punto_sino :\n  \n  hyper_exp : super_exp hyper_exp_aux\n  \n  hyper_exp_aux : push_op_logicos super_exp check_op_logicos\n                | empty\n  \n  check_op_logicos :\n  \n  push_op_logicos : Y \n        | O \n        | empty\n  \n  super_exp : exp super_exp_aux\n  \n  super_exp_aux : push_op_relacionales exp check_op_relacionales\n                | empty\n  \n  check_op_relacionales :\n  \n  push_op_relacionales : GREATER\n        | LESS \n        | GREATEREQ\n        | LESSEQ\n        | NOTEQUAL\n        | EQUAL\n  \n  exp : term check_op_masmenos exp_aux\n  \n  exp_aux : push_op_exp_masmenos exp\n          | empty\n  \n  push_op_exp_masmenos : PLUS \n        | MINUS\n  \n  check_op_masmenos :\n  \n  term : factor check_op_pordiv term_aux\n  \n  term_aux : push_op_exp_pordiv term \n        | empty\n  \n  check_op_pordiv :\n  \n  push_op_exp_pordiv : TIMES \n        | DIVIDE\n  \n  factor : LPAREN meter_fondo_falso hyper_exp RPAREN quitar_fondo_falso\n          | factor_constante\n          | llamada_func_return\n          | ID LBRACKET hyper_exp RBRACKET\n          | ID LBRACKET hyper_exp RBRACKET LBRACKET hyper_exp RBRACKET\n          | ID push_id\n  \n  factor_constante : CTEI push_int\n                | CTEF push_float\n                | CTECHAR push_char\n  \n  meter_fondo_falso :\n  \n  quitar_fondo_falso :\n  \n  push_int :\n  \n  push_float :\n  \n  push_id :\n  \n  push_char :\n  \n  func_params_aux : COMMA exp punto_check_param func_params_aux\n                  | empty\n  \n  func_params : exp punto_check_param func_params_aux\n              | empty\n  \n  punto_check_param :\n  \n  llamada_func_void : ID LPAREN punto_func_exists punto_validate_isvoid punto_create_era func_params RPAREN punto_check_total_params punto_create_gosub SEMICOLON\n  \n  llamada_func_return : ID LPAREN punto_func_exists punto_create_era func_params RPAREN punto_check_total_params punto_create_gosub\n  \n  punto_func_exists :\n  \n  punto_validate_isvoid :\n  \n  punto_create_era : \n  \n  punto_check_total_params :\n  \n  punto_create_gosub :\n  \n  imprimir : IMPRIMIR LPAREN imprimir_aux RPAREN SEMICOLON\n  imprimir_aux : exp push_imprimir imprimirCycle\n              | CTESTRING push_imprimir imprimirCycle\n  imprimirCycle : COMMA imprimir_aux\n              | empty\n  \n  push_imprimir :\n  \n  empty : \n  '
    
_lr_action_items = {'PROGRAMA':([0,],[2,]),'$end':([1,6,20,22,36,101,],[0,-1,-2,-4,-3,-6,]),'ID':([2,10,11,13,14,15,24,28,29,30,31,32,41,42,43,44,50,57,59,60,61,62,63,64,65,75,78,84,85,87,89,91,92,93,97,102,103,105,106,107,108,109,110,111,112,113,115,117,118,122,124,130,132,133,134,135,136,137,138,139,140,145,146,147,148,149,150,151,152,153,154,155,156,157,162,163,169,173,174,175,176,177,178,179,180,181,182,183,184,187,188,192,193,195,199,203,204,205,206,209,214,215,216,217,218,221,223,236,237,240,242,249,253,256,265,269,270,278,280,281,283,289,290,298,302,307,],[3,-143,-11,-15,-16,-17,-10,39,40,-18,-19,-20,47,48,49,-9,67,67,-47,-48,-49,-50,-51,-52,-53,96,98,-62,-132,110,114,110,110,-65,-21,110,-133,-103,-107,-119,-111,-112,-123,-121,-122,-124,110,-143,-143,161,-143,-134,-143,-143,110,110,-115,-132,-116,-117,-118,110,-87,-85,-86,-88,110,-90,-92,-93,-94,-95,-96,-97,-143,67,207,110,110,-98,110,-100,-101,-102,-104,110,-106,-108,-109,-134,110,-91,-137,110,67,67,110,230,-25,-56,-99,-105,-120,-113,110,67,-89,-110,110,67,-64,266,110,-135,-29,-114,-136,-130,-131,110,-76,-67,67,67,-77,-71,]),'COLON':([3,4,],[-5,5,]),'INICIO':([5,7,8,10,11,12,13,14,15,21,24,25,26,27,38,97,206,244,260,261,265,275,],[9,9,9,-143,-11,-143,-15,-16,-17,9,-10,-143,-12,-14,-13,-21,-25,-36,-36,-34,-29,-33,]),'FUNCION':([5,7,10,11,12,13,14,15,24,25,97,206,244,260,261,265,275,],[16,16,-143,-11,16,-15,-16,-17,-10,16,-21,-25,-36,-36,-34,-29,-33,]),'VARIABLE':([5,10,13,14,15,97,124,162,206,265,],[17,17,-15,-16,-17,-21,17,17,-25,-29,]),'RENGLON':([5,10,13,14,15,97,124,162,206,265,],[18,18,-15,-16,-17,-21,18,18,-25,-29,]),'TABLA':([5,10,13,14,15,97,124,162,206,265,],[19,19,-15,-16,-17,-21,19,19,-25,-29,]),'LPAREN':([9,39,40,45,46,51,67,68,69,70,71,72,84,85,87,90,91,92,102,103,105,106,107,108,109,110,111,112,113,115,117,118,130,132,133,134,135,136,137,138,139,140,145,146,147,148,149,150,151,152,153,154,155,156,157,173,174,175,176,177,178,179,180,181,182,183,184,187,188,192,195,204,214,215,216,217,218,223,236,237,253,256,269,270,271,280,281,],[23,-37,-37,-35,52,73,85,89,-68,91,92,93,-62,-132,107,115,107,107,107,-133,-103,-107,-119,-111,-112,137,-121,-122,-124,107,-143,-143,-134,-143,-143,107,107,-115,-132,-116,-117,-118,107,-87,-85,-86,-88,107,-90,-92,-93,-94,-95,-96,-97,107,107,-98,107,-100,-101,-102,-104,107,-106,-108,-109,-134,107,-91,107,107,-99,-105,-120,-113,107,-89,-110,107,107,-135,-114,-136,281,-131,107,]),'REGRESAR':([10,11,13,14,15,24,59,60,61,62,63,64,65,97,124,162,163,193,199,203,206,209,221,240,242,265,278,283,289,290,298,302,307,],[-143,-11,-15,-16,-17,-10,-47,-48,-49,-50,-51,-52,-53,-21,-143,-143,204,-137,204,204,-25,-56,204,204,-64,-29,-130,-76,-67,204,204,-77,-71,]),'DESDE':([10,11,13,14,15,24,44,50,57,59,60,61,62,63,64,65,97,124,162,163,193,199,203,206,209,221,240,242,265,278,283,289,290,298,302,307,],[-143,-11,-15,-16,-17,-10,-9,68,68,-47,-48,-49,-50,-51,-52,-53,-21,-143,-143,68,-137,68,68,-25,-56,68,68,-64,-29,-130,-76,-67,68,68,-77,-71,]),'MIENTRAS':([10,11,13,14,15,24,44,50,57,59,60,61,62,63,64,65,97,124,162,163,193,199,203,206,209,221,240,242,265,278,283,289,290,298,302,307,],[-143,-11,-15,-16,-17,-10,-9,69,69,-47,-48,-49,-50,-51,-52,-53,-21,-143,-143,69,-137,69,69,-25,-56,69,69,-64,-29,-130,-76,-67,69,69,-77,-71,]),'SI':([10,11,13,14,15,24,44,50,57,59,60,61,62,63,64,65,97,124,162,163,193,199,203,206,209,221,240,242,265,278,283,289,290,298,302,307,],[-143,-11,-15,-16,-17,-10,-9,70,70,-47,-48,-49,-50,-51,-52,-53,-21,-143,-143,70,-137,70,70,-25,-56,70,70,-64,-29,-130,-76,-67,70,70,-77,-71,]),'IMPRIMIR':([10,11,13,14,15,24,44,50,57,59,60,61,62,63,64,65,97,124,162,163,193,199,203,206,209,221,240,242,265,278,283,289,290,298,302,307,],[-143,-11,-15,-16,-17,-10,-9,71,71,-47,-48,-49,-50,-51,-52,-53,-21,-143,-143,71,-137,71,71,-25,-56,71,71,-64,-29,-130,-76,-67,71,71,-77,-71,]),'LEER':([10,11,13,14,15,24,44,50,57,59,60,61,62,63,64,65,97,124,162,163,193,199,203,206,209,221,240,242,265,278,283,289,290,298,302,307,],[-143,-11,-15,-16,-17,-10,-9,72,72,-47,-48,-49,-50,-51,-52,-53,-21,-143,-143,72,-137,72,72,-25,-56,72,72,-64,-29,-130,-76,-67,72,72,-77,-71,]),'SINREGRESAR':([16,],[29,]),'ENTERO':([16,17,18,19,52,73,165,],[30,30,30,30,30,30,30,]),'DECIMAL':([16,17,18,19,52,73,165,],[31,31,31,31,31,31,31,]),'LETRA':([16,17,18,19,52,73,165,],[32,32,32,32,32,32,32,]),'RPAREN':([23,52,73,74,76,85,94,96,103,105,106,108,109,110,111,112,113,116,117,118,119,120,121,125,130,132,133,136,137,138,139,140,142,144,146,149,151,159,160,161,164,166,173,175,177,180,182,185,187,191,192,194,196,197,198,210,211,212,214,215,216,217,218,219,222,223,224,230,234,236,238,246,252,254,256,263,268,269,270,279,280,287,288,],[37,-143,-143,95,-39,-132,123,-42,-133,-103,-107,-111,-112,-123,-121,-122,-124,143,-143,-143,158,-142,-142,-143,-134,-143,-143,-115,-132,-116,-117,-118,189,-81,-83,-88,-90,-143,-143,-66,-38,-41,-143,-98,-100,-104,-106,216,-134,-84,-91,-138,-141,-139,225,233,-129,-128,-99,-105,-120,-113,-143,239,-82,-89,-140,-42,-143,-110,256,-143,-127,-126,-135,-40,-129,-114,-136,-143,-131,-125,292,]),'ARROW':([30,31,32,33,34,35,],[-18,-19,-20,41,42,43,]),'LBRACE':([37,95,123,143,189,190,220,274,284,292,295,],[44,124,162,-78,-69,221,240,-80,290,-74,298,]),'RBRACE':([44,50,56,57,58,59,60,61,62,63,64,65,83,193,200,201,202,203,209,226,228,241,242,245,258,262,278,283,289,293,301,302,307,],[-9,-143,82,-143,-8,-47,-48,-49,-50,-51,-52,-53,-7,-137,227,-43,-44,-46,-56,243,-45,259,-64,-55,272,-54,-130,-76,-67,296,304,-77,-71,]),'COMMA':([47,53,96,98,99,105,106,108,109,110,111,112,113,120,121,125,126,127,132,133,136,138,139,140,159,160,175,177,180,182,208,211,214,215,216,217,230,232,234,236,246,256,264,268,269,270,276,279,280,300,303,],[-24,78,-42,-24,-28,-103,-107,-111,-112,-123,-121,-122,-124,-142,-142,165,78,169,-143,-143,-115,-116,-117,-118,195,195,-98,-100,-104,-106,-32,-129,-99,-105,-120,-113,-42,249,253,-110,165,-135,-28,-129,-114,-136,169,253,-131,-32,249,]),'SEMICOLON':([47,53,77,79,82,98,99,105,106,108,109,110,111,112,113,117,118,126,127,129,132,133,136,138,139,140,144,146,149,151,158,167,168,170,172,175,177,180,182,191,192,208,214,215,216,217,222,223,225,227,229,232,233,236,243,248,250,251,256,259,264,267,269,270,272,273,276,280,282,285,296,299,300,303,304,305,306,],[-24,-143,97,-23,101,-24,-28,-103,-107,-111,-112,-123,-121,-122,-124,-143,-143,-143,-143,-63,-143,-143,-115,-116,-117,-118,-81,-83,-88,-90,193,-22,206,-27,209,-98,-100,-104,-106,-84,-91,-32,-99,-105,-120,-113,-82,-89,242,244,245,-143,-135,-110,260,265,-31,-136,-135,-79,-28,278,-114,-136,-70,283,-143,-131,289,-26,-79,302,-32,-143,-75,-30,307,]),'LBRACKET':([48,49,67,100,110,131,207,217,266,291,],[54,55,87,128,135,174,231,237,277,294,]),'CTEI':([54,55,84,85,87,91,92,102,103,105,106,107,108,109,110,111,112,113,115,117,118,128,130,132,133,134,135,136,137,138,139,140,145,146,147,148,149,150,151,152,153,154,155,156,157,173,174,175,176,177,178,179,180,181,182,183,184,187,188,192,195,204,214,215,216,217,218,223,231,236,237,253,256,269,270,277,280,281,294,],[80,81,-62,-132,111,111,111,111,-133,-103,-107,-119,-111,-112,-123,-121,-122,-124,111,-143,-143,171,-134,-143,-143,111,111,-115,-132,-116,-117,-118,111,-87,-85,-86,-88,111,-90,-92,-93,-94,-95,-96,-97,111,111,-98,111,-100,-101,-102,-104,111,-106,-108,-109,-134,111,-91,111,111,-99,-105,-120,-113,111,-89,247,-110,111,111,-135,-114,-136,286,-131,111,297,]),'ASSIGN':([66,67,86,88,114,131,141,235,],[84,-61,-57,-60,-72,-58,188,-59,]),'RBRACKET':([80,81,104,105,106,108,109,110,111,112,113,117,118,132,133,136,138,139,140,144,146,149,151,171,175,177,180,182,186,191,192,213,214,215,216,217,222,223,236,247,255,256,269,270,280,286,297,],[99,100,131,-103,-107,-111,-112,-123,-121,-122,-124,-143,-143,-143,-143,-115,-116,-117,-118,-81,-83,-88,-90,208,-98,-100,-104,-106,217,-84,-91,235,-99,-105,-120,-113,-82,-89,-110,264,269,-135,-114,-136,-131,291,300,]),'CTEF':([84,85,87,91,92,102,103,105,106,107,108,109,110,111,112,113,115,117,118,130,132,133,134,135,136,137,138,139,140,145,146,147,148,149,150,151,152,153,154,155,156,157,173,174,175,176,177,178,179,180,181,182,183,184,187,188,192,195,204,214,215,216,217,218,223,236,237,253,256,269,270,280,281,],[-62,-132,112,112,112,112,-133,-103,-107,-119,-111,-112,-123,-121,-122,-124,112,-143,-143,-134,-143,-143,112,112,-115,-132,-116,-117,-118,112,-87,-85,-86,-88,112,-90,-92,-93,-94,-95,-96,-97,112,112,-98,112,-100,-101,-102,-104,112,-106,-108,-109,-134,112,-91,112,112,-99,-105,-120,-113,112,-89,-110,112,112,-135,-114,-136,-131,112,]),'CTECHAR':([84,85,87,91,92,102,103,105,106,107,108,109,110,111,112,113,115,117,118,130,132,133,134,135,136,137,138,139,140,145,146,147,148,149,150,151,152,153,154,155,156,157,173,174,175,176,177,178,179,180,181,182,183,184,187,188,192,195,204,214,215,216,217,218,223,236,237,253,256,269,270,280,281,],[-62,-132,113,113,113,113,-133,-103,-107,-119,-111,-112,-123,-121,-122,-124,113,-143,-143,-134,-143,-143,113,113,-115,-132,-116,-117,-118,113,-87,-85,-86,-88,113,-90,-92,-93,-94,-95,-96,-97,113,113,-98,113,-100,-101,-102,-104,113,-106,-108,-109,-134,113,-91,113,113,-99,-105,-120,-113,113,-89,-110,113,113,-135,-114,-136,-131,113,]),'CTESTRING':([92,195,],[121,121,]),'PLUS':([105,106,108,109,110,111,112,113,132,133,136,138,139,140,180,182,215,216,217,236,256,269,270,280,],[-103,-107,-111,-112,-123,-121,-122,-124,178,-143,-115,-116,-117,-118,-104,-106,-105,-120,-113,-110,-135,-114,-136,-131,]),'MINUS':([105,106,108,109,110,111,112,113,132,133,136,138,139,140,180,182,215,216,217,236,256,269,270,280,],[-103,-107,-111,-112,-123,-121,-122,-124,179,-143,-115,-116,-117,-118,-104,-106,-105,-120,-113,-110,-135,-114,-136,-131,]),'GREATER':([105,106,108,109,110,111,112,113,118,132,133,136,138,139,140,175,177,180,182,214,215,216,217,236,256,269,270,280,],[-103,-107,-111,-112,-123,-121,-122,-124,152,-143,-143,-115,-116,-117,-118,-98,-100,-104,-106,-99,-105,-120,-113,-110,-135,-114,-136,-131,]),'LESS':([105,106,108,109,110,111,112,113,118,132,133,136,138,139,140,175,177,180,182,214,215,216,217,236,256,269,270,280,],[-103,-107,-111,-112,-123,-121,-122,-124,153,-143,-143,-115,-116,-117,-118,-98,-100,-104,-106,-99,-105,-120,-113,-110,-135,-114,-136,-131,]),'GREATEREQ':([105,106,108,109,110,111,112,113,118,132,133,136,138,139,140,175,177,180,182,214,215,216,217,236,256,269,270,280,],[-103,-107,-111,-112,-123,-121,-122,-124,154,-143,-143,-115,-116,-117,-118,-98,-100,-104,-106,-99,-105,-120,-113,-110,-135,-114,-136,-131,]),'LESSEQ':([105,106,108,109,110,111,112,113,118,132,133,136,138,139,140,175,177,180,182,214,215,216,217,236,256,269,270,280,],[-103,-107,-111,-112,-123,-121,-122,-124,155,-143,-143,-115,-116,-117,-118,-98,-100,-104,-106,-99,-105,-120,-113,-110,-135,-114,-136,-131,]),'NOTEQUAL':([105,106,108,109,110,111,112,113,118,132,133,136,138,139,140,175,177,180,182,214,215,216,217,236,256,269,270,280,],[-103,-107,-111,-112,-123,-121,-122,-124,156,-143,-143,-115,-116,-117,-118,-98,-100,-104,-106,-99,-105,-120,-113,-110,-135,-114,-136,-131,]),'EQUAL':([105,106,108,109,110,111,112,113,118,132,133,136,138,139,140,175,177,180,182,214,215,216,217,236,256,269,270,280,],[-103,-107,-111,-112,-123,-121,-122,-124,157,-143,-143,-115,-116,-117,-118,-98,-100,-104,-106,-99,-105,-120,-113,-110,-135,-114,-136,-131,]),'Y':([105,106,108,109,110,111,112,113,117,118,132,133,136,138,139,140,149,151,175,177,180,182,192,214,215,216,217,223,236,256,269,270,280,],[-103,-107,-111,-112,-123,-121,-122,-124,147,-143,-143,-143,-115,-116,-117,-118,-88,-90,-98,-100,-104,-106,-91,-99,-105,-120,-113,-89,-110,-135,-114,-136,-131,]),'O':([105,106,108,109,110,111,112,113,117,118,132,133,136,138,139,140,149,151,175,177,180,182,192,214,215,216,217,223,236,256,269,270,280,],[-103,-107,-111,-112,-123,-121,-122,-124,148,-143,-143,-143,-115,-116,-117,-118,-88,-90,-98,-100,-104,-106,-91,-99,-105,-120,-113,-89,-110,-135,-114,-136,-131,]),'TIMES':([106,108,109,110,111,112,113,133,136,138,139,140,216,217,236,256,269,270,280,],[-107,-111,-112,-123,-121,-122,-124,183,-115,-116,-117,-118,-120,-113,-110,-135,-114,-136,-131,]),'DIVIDE':([106,108,109,110,111,112,113,133,136,138,139,140,216,217,236,256,269,270,280,],[-107,-111,-112,-123,-121,-122,-124,184,-115,-116,-117,-118,-120,-113,-110,-135,-114,-136,-131,]),'HASTA':([239,257,],[-73,271,]),'SINO':([259,],[274,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programa':([0,],[1,]),'punto_programa':([3,],[4,]),'inicio':([5,7,8,21,],[6,20,22,36,]),'dec_var_cycle':([5,10,124,162,],[7,24,163,199,]),'dec_func_cycle':([5,7,],[8,21,]),'dec_var':([5,10,124,162,],[10,10,10,10,]),'empty':([5,10,12,25,50,52,53,57,73,117,118,124,125,126,127,132,133,159,160,162,173,218,232,234,246,276,279,303,],[11,11,27,27,58,76,79,58,76,146,151,11,166,79,170,177,182,196,196,11,212,212,250,254,166,170,254,250,]),'dec_func':([5,7,12,25,],[12,12,25,25,]),'simple_var':([5,10,124,162,],[13,13,13,13,]),'array':([5,10,124,162,],[14,14,14,14,]),'matrix':([5,10,124,162,],[15,15,15,15,]),'p_dec_func_aux':([12,25,],[26,38,]),'type':([16,17,18,19,52,73,165,],[28,33,34,35,75,75,205,]),'punto_add_func':([39,40,],[45,46,]),'punto_update_goto':([44,],[50,]),'punto_global_func_var':([45,],[51,]),'punto_simple_var':([47,98,],[53,126,]),'inicio_estatutos':([50,57,],[56,83,]),'estatutos_opciones':([50,57,163,199,203,221,240,290,298,],[57,57,203,203,203,203,203,203,203,]),'asignar':([50,57,163,199,203,221,240,290,298,],[59,59,59,59,59,59,59,59,59,]),'llamada_func_void':([50,57,163,199,203,221,240,290,298,],[60,60,60,60,60,60,60,60,60,]),'ciclo_for':([50,57,163,199,203,221,240,290,298,],[61,61,61,61,61,61,61,61,61,]),'ciclo_while':([50,57,163,199,203,221,240,290,298,],[62,62,62,62,62,62,62,62,62,]),'condicion':([50,57,163,199,203,221,240,290,298,],[63,63,63,63,63,63,63,63,63,]),'imprimir':([50,57,163,199,203,221,240,290,298,],[64,64,64,64,64,64,64,64,64,]),'leer':([50,57,163,199,203,221,240,290,298,],[65,65,65,65,65,65,65,65,65,]),'variable':([50,57,163,199,203,221,240,290,298,],[66,66,66,66,66,66,66,66,66,]),'parameter':([52,73,],[74,94,]),'simpleVarCycle':([53,126,],[77,167,]),'variable_aux':([67,],[86,]),'punto_push_id':([67,],[88,]),'punto_inicio_while':([69,],[90,]),'push_op_igual':([84,],[102,]),'punto_func_exists':([85,137,],[103,187,]),'exp':([87,91,92,102,115,134,135,145,150,173,174,176,188,195,204,218,237,253,281,],[104,118,120,118,118,118,118,118,192,211,213,214,118,120,229,211,118,268,118,]),'term':([87,91,92,102,115,134,135,145,150,173,174,176,181,188,195,204,218,237,253,281,],[105,105,105,105,105,105,105,105,105,105,105,105,215,105,105,105,105,105,105,105,]),'factor':([87,91,92,102,115,134,135,145,150,173,174,176,181,188,195,204,218,237,253,281,],[106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,]),'factor_constante':([87,91,92,102,115,134,135,145,150,173,174,176,181,188,195,204,218,237,253,281,],[108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,]),'llamada_func_return':([87,91,92,102,115,134,135,145,150,173,174,176,181,188,195,204,218,237,253,281,],[109,109,109,109,109,109,109,109,109,109,109,109,109,109,109,109,109,109,109,109,]),'hyper_exp':([91,102,115,134,135,188,237,281,],[116,129,142,185,186,219,255,288,]),'super_exp':([91,102,115,134,135,145,188,237,281,],[117,117,117,117,117,191,117,117,117,]),'imprimir_aux':([92,195,],[119,224,]),'punto_push_leer':([93,],[122,]),'punto_add_parameter':([96,230,],[125,246,]),'punto_array':([99,264,],[127,276,]),'punto_validate_isvoid':([103,],[130,]),'check_op_masmenos':([105,],[132,]),'check_op_pordiv':([106,],[133,]),'meter_fondo_falso':([107,],[134,]),'push_id':([110,],[136,]),'push_int':([111,],[138,]),'push_float':([112,],[139,]),'push_char':([113,],[140,]),'punto_existe_id':([114,],[141,]),'hyper_exp_aux':([117,],[144,]),'push_op_logicos':([117,],[145,]),'super_exp_aux':([118,],[149,]),'push_op_relacionales':([118,],[150,]),'push_imprimir':([120,121,],[159,160,]),'parameterCycle':([125,246,],[164,263,]),'arrayCycle':([127,276,],[168,285,]),'check_op_igual':([129,],[172,]),'punto_create_era':([130,187,],[173,218,]),'exp_aux':([132,],[175,]),'push_op_exp_masmenos':([132,],[176,]),'term_aux':([133,],[180,]),'push_op_exp_pordiv':([133,],[181,]),'punto_si':([143,],[190,]),'imprimirCycle':([159,160,],[194,197,]),'punto_create_leer':([161,],[198,]),'estatutos':([163,199,203,221,240,290,298,],[200,226,228,241,258,293,301,]),'estatutosCycle':([163,199,203,221,240,290,298,],[201,201,201,201,201,201,201,]),'func_regresar':([163,199,203,221,240,290,298,],[202,202,202,202,202,202,202,]),'func_params':([173,218,],[210,238,]),'punto_medio_while':([189,],[220,]),'check_op_logicos':([191,],[222,]),'check_op_relacionales':([192,],[223,]),'punto_matrix':([208,300,],[232,303,]),'punto_check_param':([211,268,],[234,279,]),'quitar_fondo_falso':([216,],[236,]),'matrixCycle':([232,303,],[248,305,]),'punto_check_total_params':([233,256,],[251,270,]),'func_params_aux':([234,279,],[252,287,]),'punto_valida_int':([239,],[257,]),'punto_end_function':([244,260,],[261,275,]),'punto_check_types':([245,],[262,]),'punto_create_gosub':([251,270,],[267,280,]),'punto_fin_si':([259,296,],[273,299,]),'punto_fin_while':([272,],[282,]),'punto_sino':([274,],[284,]),'punto_valida_exp':([292,],[295,]),'punto_termina_for':([304,],[306,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> PROGRAMA ID punto_programa COLON inicio','programa',5,'p_programa','parser_frima.py',33),
  ('programa -> PROGRAMA ID punto_programa COLON dec_var_cycle inicio','programa',6,'p_programa','parser_frima.py',34),
  ('programa -> PROGRAMA ID punto_programa COLON dec_var_cycle dec_func_cycle inicio','programa',7,'p_programa','parser_frima.py',35),
  ('programa -> PROGRAMA ID punto_programa COLON dec_func_cycle inicio','programa',6,'p_programa','parser_frima.py',36),
  ('punto_programa -> <empty>','punto_programa',0,'p_punto_programa','parser_frima.py',43),
  ('inicio -> INICIO LPAREN RPAREN LBRACE punto_update_goto inicio_estatutos RBRACE SEMICOLON','inicio',8,'p_inicio','parser_frima.py',55),
  ('inicio_estatutos -> estatutos_opciones inicio_estatutos','inicio_estatutos',2,'p_inicio_estatutos','parser_frima.py',65),
  ('inicio_estatutos -> empty','inicio_estatutos',1,'p_inicio_estatutos','parser_frima.py',66),
  ('punto_update_goto -> <empty>','punto_update_goto',0,'p_punto_update_goto','parser_frima.py',72),
  ('dec_var_cycle -> dec_var dec_var_cycle','dec_var_cycle',2,'p_dec_var_cycle','parser_frima.py',81),
  ('dec_var_cycle -> empty','dec_var_cycle',1,'p_dec_var_cycle','parser_frima.py',82),
  ('dec_func_cycle -> dec_func p_dec_func_aux','dec_func_cycle',2,'p_dec_func_cycle','parser_frima.py',88),
  ('p_dec_func_aux -> dec_func p_dec_func_aux','p_dec_func_aux',2,'p_dec_func_aux','parser_frima.py',93),
  ('p_dec_func_aux -> empty','p_dec_func_aux',1,'p_dec_func_aux','parser_frima.py',94),
  ('dec_var -> simple_var','dec_var',1,'p_dec_var','parser_frima.py',100),
  ('dec_var -> array','dec_var',1,'p_dec_var','parser_frima.py',101),
  ('dec_var -> matrix','dec_var',1,'p_dec_var','parser_frima.py',102),
  ('type -> ENTERO','type',1,'p_type','parser_frima.py',110),
  ('type -> DECIMAL','type',1,'p_type','parser_frima.py',111),
  ('type -> LETRA','type',1,'p_type','parser_frima.py',112),
  ('simple_var -> VARIABLE type ARROW ID punto_simple_var simpleVarCycle SEMICOLON','simple_var',7,'p_simple_var','parser_frima.py',122),
  ('simpleVarCycle -> COMMA ID punto_simple_var simpleVarCycle','simpleVarCycle',4,'p_simple_var','parser_frima.py',123),
  ('simpleVarCycle -> empty','simpleVarCycle',1,'p_simple_var','parser_frima.py',124),
  ('punto_simple_var -> <empty>','punto_simple_var',0,'p_punto_simple_var','parser_frima.py',131),
  ('array -> RENGLON type ARROW ID LBRACKET CTEI RBRACKET punto_array arrayCycle SEMICOLON','array',10,'p_array','parser_frima.py',139),
  ('arrayCycle -> COMMA ID LBRACKET CTEI RBRACKET punto_array arrayCycle','arrayCycle',7,'p_array','parser_frima.py',140),
  ('arrayCycle -> empty','arrayCycle',1,'p_array','parser_frima.py',141),
  ('punto_array -> <empty>','punto_array',0,'p_punto_array','parser_frima.py',149),
  ('matrix -> TABLA type ARROW ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET punto_matrix matrixCycle SEMICOLON','matrix',13,'p_matrix','parser_frima.py',156),
  ('matrixCycle -> COMMA ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET punto_matrix matrixCycle','matrixCycle',10,'p_matrix','parser_frima.py',157),
  ('matrixCycle -> empty','matrixCycle',1,'p_matrix','parser_frima.py',158),
  ('punto_matrix -> <empty>','punto_matrix',0,'p_punto_matrix','parser_frima.py',166),
  ('dec_func -> FUNCION type ID punto_add_func punto_global_func_var LPAREN parameter RPAREN LBRACE dec_var_cycle estatutos RBRACE SEMICOLON punto_end_function','dec_func',14,'p_dec_func','parser_frima.py',173),
  ('dec_func -> FUNCION SINREGRESAR ID punto_add_func LPAREN parameter RPAREN LBRACE dec_var_cycle estatutos RBRACE SEMICOLON punto_end_function','dec_func',13,'p_dec_func','parser_frima.py',174),
  ('punto_global_func_var -> <empty>','punto_global_func_var',0,'p_punto_global_func_var','parser_frima.py',179),
  ('punto_end_function -> <empty>','punto_end_function',0,'p_punto_end_function','parser_frima.py',190),
  ('punto_add_func -> <empty>','punto_add_func',0,'p_punto_add_func','parser_frima.py',206),
  ('parameter -> type ID punto_add_parameter parameterCycle','parameter',4,'p_parameter','parser_frima.py',215),
  ('parameter -> empty','parameter',1,'p_parameter','parser_frima.py',216),
  ('parameterCycle -> COMMA type ID punto_add_parameter parameterCycle','parameterCycle',5,'p_parameterCycle','parser_frima.py',223),
  ('parameterCycle -> empty','parameterCycle',1,'p_parameterCycle','parser_frima.py',224),
  ('punto_add_parameter -> <empty>','punto_add_parameter',0,'p_punto_add_parameter','parser_frima.py',231),
  ('estatutos -> estatutosCycle','estatutos',1,'p_estatutos','parser_frima.py',240),
  ('estatutos -> func_regresar','estatutos',1,'p_estatutos','parser_frima.py',241),
  ('estatutosCycle -> estatutos_opciones estatutos','estatutosCycle',2,'p_estatutosCycle','parser_frima.py',247),
  ('estatutosCycle -> estatutos_opciones','estatutosCycle',1,'p_estatutosCycle','parser_frima.py',248),
  ('estatutos_opciones -> asignar','estatutos_opciones',1,'p_estatutos_opciones','parser_frima.py',254),
  ('estatutos_opciones -> llamada_func_void','estatutos_opciones',1,'p_estatutos_opciones','parser_frima.py',255),
  ('estatutos_opciones -> ciclo_for','estatutos_opciones',1,'p_estatutos_opciones','parser_frima.py',256),
  ('estatutos_opciones -> ciclo_while','estatutos_opciones',1,'p_estatutos_opciones','parser_frima.py',257),
  ('estatutos_opciones -> condicion','estatutos_opciones',1,'p_estatutos_opciones','parser_frima.py',258),
  ('estatutos_opciones -> imprimir','estatutos_opciones',1,'p_estatutos_opciones','parser_frima.py',259),
  ('estatutos_opciones -> leer','estatutos_opciones',1,'p_estatutos_opciones','parser_frima.py',260),
  ('func_regresar -> REGRESAR exp SEMICOLON punto_check_types','func_regresar',4,'p_func_regresar','parser_frima.py',266),
  ('punto_check_types -> <empty>','punto_check_types',0,'p_punto_check_types','parser_frima.py',274),
  ('asignar -> variable ASSIGN push_op_igual hyper_exp check_op_igual SEMICOLON','asignar',6,'p_asignar','parser_frima.py',288),
  ('variable -> ID variable_aux','variable',2,'p_variable','parser_frima.py',294),
  ('variable_aux -> LBRACKET exp RBRACKET','variable_aux',3,'p_variable_aux','parser_frima.py',301),
  ('variable_aux -> LBRACKET exp RBRACKET LBRACKET exp RBRACKET','variable_aux',6,'p_variable_aux','parser_frima.py',302),
  ('variable_aux -> punto_push_id','variable_aux',1,'p_variable_aux','parser_frima.py',303),
  ('punto_push_id -> <empty>','punto_push_id',0,'p_punto_push_id','parser_frima.py',309),
  ('push_op_igual -> <empty>','push_op_igual',0,'p_push_op_igual','parser_frima.py',321),
  ('check_op_igual -> <empty>','check_op_igual',0,'p_check_op_igual','parser_frima.py',329),
  ('leer -> LEER LPAREN punto_push_leer ID punto_create_leer RPAREN SEMICOLON','leer',7,'p_leer','parser_frima.py',355),
  ('punto_push_leer -> <empty>','punto_push_leer',0,'p_punto_push_leer','parser_frima.py',360),
  ('punto_create_leer -> <empty>','punto_create_leer',0,'p_punto_create_leer','parser_frima.py',368),
  ('ciclo_while -> MIENTRAS punto_inicio_while LPAREN hyper_exp RPAREN punto_medio_while LBRACE estatutos RBRACE punto_fin_while SEMICOLON','ciclo_while',11,'p_ciclo_while','parser_frima.py',383),
  ('punto_inicio_while -> <empty>','punto_inicio_while',0,'p_punto_inicio_while','parser_frima.py',390),
  ('punto_medio_while -> <empty>','punto_medio_while',0,'p_punto_medio_while','parser_frima.py',400),
  ('punto_fin_while -> <empty>','punto_fin_while',0,'p_punto_fin_while','parser_frima.py',415),
  ('ciclo_for -> DESDE LPAREN ID punto_existe_id ASSIGN hyper_exp RPAREN punto_valida_int HASTA LPAREN hyper_exp RPAREN punto_valida_exp LBRACE estatutos RBRACE punto_termina_for SEMICOLON','ciclo_for',18,'p_ciclo_for','parser_frima.py',426),
  ('punto_existe_id -> <empty>','punto_existe_id',0,'p_punto_existe_id','parser_frima.py',434),
  ('punto_valida_int -> <empty>','punto_valida_int',0,'p_punto_valida_int','parser_frima.py',447),
  ('punto_valida_exp -> <empty>','punto_valida_exp',0,'p_punto_valida_exp','parser_frima.py',464),
  ('punto_termina_for -> <empty>','punto_termina_for',0,'p_punto_termina_for','parser_frima.py',487),
  ('condicion -> SI LPAREN hyper_exp RPAREN punto_si LBRACE estatutos RBRACE punto_fin_si SEMICOLON','condicion',10,'p_condicion','parser_frima.py',511),
  ('condicion -> SI LPAREN hyper_exp RPAREN punto_si LBRACE estatutos RBRACE SINO punto_sino LBRACE estatutos RBRACE punto_fin_si SEMICOLON','condicion',15,'p_condicion','parser_frima.py',512),
  ('punto_si -> <empty>','punto_si',0,'p_punto_si','parser_frima.py',521),
  ('punto_fin_si -> <empty>','punto_fin_si',0,'p_punto_fin_si','parser_frima.py',536),
  ('punto_sino -> <empty>','punto_sino',0,'p_punto_sino','parser_frima.py',545),
  ('hyper_exp -> super_exp hyper_exp_aux','hyper_exp',2,'p_hyper_exp','parser_frima.py',557),
  ('hyper_exp_aux -> push_op_logicos super_exp check_op_logicos','hyper_exp_aux',3,'p_hyper_exp_aux','parser_frima.py',562),
  ('hyper_exp_aux -> empty','hyper_exp_aux',1,'p_hyper_exp_aux','parser_frima.py',563),
  ('check_op_logicos -> <empty>','check_op_logicos',0,'p_check_op_logicos','parser_frima.py',570),
  ('push_op_logicos -> Y','push_op_logicos',1,'p_push_op_logicos','parser_frima.py',604),
  ('push_op_logicos -> O','push_op_logicos',1,'p_push_op_logicos','parser_frima.py',605),
  ('push_op_logicos -> empty','push_op_logicos',1,'p_push_op_logicos','parser_frima.py',606),
  ('super_exp -> exp super_exp_aux','super_exp',2,'p_super_exp','parser_frima.py',613),
  ('super_exp_aux -> push_op_relacionales exp check_op_relacionales','super_exp_aux',3,'p_super_exp_aux','parser_frima.py',618),
  ('super_exp_aux -> empty','super_exp_aux',1,'p_super_exp_aux','parser_frima.py',619),
  ('check_op_relacionales -> <empty>','check_op_relacionales',0,'p_check_op_relacionales','parser_frima.py',626),
  ('push_op_relacionales -> GREATER','push_op_relacionales',1,'p_push_op_relacionales','parser_frima.py',659),
  ('push_op_relacionales -> LESS','push_op_relacionales',1,'p_push_op_relacionales','parser_frima.py',660),
  ('push_op_relacionales -> GREATEREQ','push_op_relacionales',1,'p_push_op_relacionales','parser_frima.py',661),
  ('push_op_relacionales -> LESSEQ','push_op_relacionales',1,'p_push_op_relacionales','parser_frima.py',662),
  ('push_op_relacionales -> NOTEQUAL','push_op_relacionales',1,'p_push_op_relacionales','parser_frima.py',663),
  ('push_op_relacionales -> EQUAL','push_op_relacionales',1,'p_push_op_relacionales','parser_frima.py',664),
  ('exp -> term check_op_masmenos exp_aux','exp',3,'p_exp','parser_frima.py',671),
  ('exp_aux -> push_op_exp_masmenos exp','exp_aux',2,'p_exp_aux','parser_frima.py',676),
  ('exp_aux -> empty','exp_aux',1,'p_exp_aux','parser_frima.py',677),
  ('push_op_exp_masmenos -> PLUS','push_op_exp_masmenos',1,'p_push_op_exp_masmenos','parser_frima.py',683),
  ('push_op_exp_masmenos -> MINUS','push_op_exp_masmenos',1,'p_push_op_exp_masmenos','parser_frima.py',684),
  ('check_op_masmenos -> <empty>','check_op_masmenos',0,'p_check_op_masmenos','parser_frima.py',692),
  ('term -> factor check_op_pordiv term_aux','term',3,'p_term','parser_frima.py',722),
  ('term_aux -> push_op_exp_pordiv term','term_aux',2,'p_term_aux','parser_frima.py',728),
  ('term_aux -> empty','term_aux',1,'p_term_aux','parser_frima.py',729),
  ('check_op_pordiv -> <empty>','check_op_pordiv',0,'p_check_op_pordiv','parser_frima.py',736),
  ('push_op_exp_pordiv -> TIMES','push_op_exp_pordiv',1,'p_push_op_exp_pordiv','parser_frima.py',767),
  ('push_op_exp_pordiv -> DIVIDE','push_op_exp_pordiv',1,'p_push_op_exp_pordiv','parser_frima.py',768),
  ('factor -> LPAREN meter_fondo_falso hyper_exp RPAREN quitar_fondo_falso','factor',5,'p_factor','parser_frima.py',775),
  ('factor -> factor_constante','factor',1,'p_factor','parser_frima.py',776),
  ('factor -> llamada_func_return','factor',1,'p_factor','parser_frima.py',777),
  ('factor -> ID LBRACKET hyper_exp RBRACKET','factor',4,'p_factor','parser_frima.py',778),
  ('factor -> ID LBRACKET hyper_exp RBRACKET LBRACKET hyper_exp RBRACKET','factor',7,'p_factor','parser_frima.py',779),
  ('factor -> ID push_id','factor',2,'p_factor','parser_frima.py',780),
  ('factor_constante -> CTEI push_int','factor_constante',2,'p_factor_constante','parser_frima.py',787),
  ('factor_constante -> CTEF push_float','factor_constante',2,'p_factor_constante','parser_frima.py',788),
  ('factor_constante -> CTECHAR push_char','factor_constante',2,'p_factor_constante','parser_frima.py',789),
  ('meter_fondo_falso -> <empty>','meter_fondo_falso',0,'p_meter_fondo_falso','parser_frima.py',796),
  ('quitar_fondo_falso -> <empty>','quitar_fondo_falso',0,'p_quitar_fondo_falso','parser_frima.py',803),
  ('push_int -> <empty>','push_int',0,'p_push_int','parser_frima.py',811),
  ('push_float -> <empty>','push_float',0,'p_push_float','parser_frima.py',827),
  ('push_id -> <empty>','push_id',0,'p_push_id','parser_frima.py',842),
  ('push_char -> <empty>','push_char',0,'p_push_char','parser_frima.py',859),
  ('func_params_aux -> COMMA exp punto_check_param func_params_aux','func_params_aux',4,'p_func_params_aux','parser_frima.py',874),
  ('func_params_aux -> empty','func_params_aux',1,'p_func_params_aux','parser_frima.py',875),
  ('func_params -> exp punto_check_param func_params_aux','func_params',3,'p_func_params','parser_frima.py',881),
  ('func_params -> empty','func_params',1,'p_func_params','parser_frima.py',882),
  ('punto_check_param -> <empty>','punto_check_param',0,'p_punto_check_param','parser_frima.py',889),
  ('llamada_func_void -> ID LPAREN punto_func_exists punto_validate_isvoid punto_create_era func_params RPAREN punto_check_total_params punto_create_gosub SEMICOLON','llamada_func_void',10,'p_llamada_func_void','parser_frima.py',911),
  ('llamada_func_return -> ID LPAREN punto_func_exists punto_create_era func_params RPAREN punto_check_total_params punto_create_gosub','llamada_func_return',8,'p_llamada_func_return','parser_frima.py',917),
  ('punto_func_exists -> <empty>','punto_func_exists',0,'p_punto_func_exists','parser_frima.py',923),
  ('punto_validate_isvoid -> <empty>','punto_validate_isvoid',0,'p_punto_validate_isvoid','parser_frima.py',934),
  ('punto_create_era -> <empty>','punto_create_era',0,'p_punto_create_era','parser_frima.py',943),
  ('punto_check_total_params -> <empty>','punto_check_total_params',0,'p_punto_check_total_params','parser_frima.py',958),
  ('punto_create_gosub -> <empty>','punto_create_gosub',0,'p_punto_create_gosub','parser_frima.py',970),
  ('imprimir -> IMPRIMIR LPAREN imprimir_aux RPAREN SEMICOLON','imprimir',5,'p_imprimir','parser_frima.py',990),
  ('imprimir_aux -> exp push_imprimir imprimirCycle','imprimir_aux',3,'p_imprimir','parser_frima.py',991),
  ('imprimir_aux -> CTESTRING push_imprimir imprimirCycle','imprimir_aux',3,'p_imprimir','parser_frima.py',992),
  ('imprimirCycle -> COMMA imprimir_aux','imprimirCycle',2,'p_imprimir','parser_frima.py',993),
  ('imprimirCycle -> empty','imprimirCycle',1,'p_imprimir','parser_frima.py',994),
  ('push_imprimir -> <empty>','push_imprimir',0,'p_push_imprimir','parser_frima.py',1003),
  ('empty -> <empty>','empty',0,'p_empty','parser_frima.py',1022),
]
