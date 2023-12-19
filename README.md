
create table students(admission_no char(4) primary key,
 cash_in_hand float not null default 5000,
 hdfc float default 0 ,
 uco float default 0 ,
 zomato float default 0 ,
 hindustan_uni float default 0 ,
 cipla float default 0 ,
 tata float default 0,
 check(cash_in_hand >=0),
 check(hdfc >=0),
 check(uco>=0),
 check(zomato>=0),
 check(hindustan_uni>=0),
 check(tata>=0)
 );