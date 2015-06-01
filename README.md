# Apache Ambari integration for Spring XD

To compile with different stacks:

```text
$ mvn clean package -P phd
$ mvn clean package -P hdp
```
Install into Ambari Server via rpm's in `target/rpm/springxd-plugin-hdp/RPMS/noarch/`.

