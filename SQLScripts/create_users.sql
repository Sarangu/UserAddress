USE UserAddress;

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE user (
  user_no integer NOT NULL AUTO_INCREMENT,
  last_name varchar(25) DEFAULT NULL,
  first_name varchar(25) DEFAULT NULL,
  email varchar(45) DEFAULT NULL,
  phone_number varchar(20) UNIQUE NOT NULL,
  `created_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

INSERT INTO user (last_name, first_name, email, phone_number) VALUES ('Geller', 'Ross', 'ross.geller@gmail.com', 'xxxxxxxxxx'),
                                                                     ('Geller', 'Monica', 'monica.geller@gmail.com', 'yyxxxxxxxx'),
                                                                     ('Greene', 'Rachel', 'rachel.greene@gmail.com', 'xxxxxxxxyy'),
                                                                     ('Tribbiani', 'Joey', 'joey.tribbiani@gmail.com', 'yyyyyyyyyyy'),
                                                                     ('Bing', 'Chandler', 'chandler.bing@gmail.com', 'xxyxxxxxxx'),
                                                                     ('Buffay', 'Phoebe', 'phoebe.buffay@gmail.com', 'xxxxyyxxxx'),
                                                                     ('Stark', 'Arya', 'arya.stark@gmail.com', 'xxxxxxxyzx');

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE address (
  street_number integer NOT NULL,
  street_name1 varchar(25) DEFAULT NULL,
  street_name2 varchar(25) DEFAULT NULL,
  city varchar(45) NOT NULL,
  state varchar(20) NOT NULL,
  postal_code varchar(10) NOT NULL,
  user_number integer NOT NULL,
  FOREIGN KEY (user_number) REFERENCES user(user_no) on delete cascade
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

INSERT INTO address (street_number, street_name1, city, state, postal_code, user_number)
                    VALUES (49, 'Roosevelt St.', 'Bronx', 'NY', '10461', 1),
                           (81, 'Atlantic Drive', 'Astoria', 'NY', '11103', 1),
                           (280, 'Honey Creek Dr.', 'Tonawanda', 'NY', '14150', 2),
                           (7490, 'Catherine Road', 'Patchogue', 'NY', '11772', 4),
                           (512, 'Vernon Dr.', 'Buffalo', 'NY', '14221', 7);