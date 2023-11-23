select num_pedido,disponibleinicio || "-" || disponiblefin,(disponiblefin-disponibleinicio+1)Stock from pedidos
where rncyfs ="AB"
order by disponibleinicio