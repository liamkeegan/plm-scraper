# plm-scraper
Screen scraper for Cisco PLM licensing usage table

Ever need to grab the output of a Cisco CUCM PLM licensing tool? This does the job for you, using the Selenium web toolkit, a headless Chrome browser and a few libraries.

Once it retrieves and formats it, it sends the output to a WebEx Teams room.

Run it with a Cron Job and you're all set.

Here's a sample output:

```
+-------------------------------------------------------------------------------------------------------------+
|                                              TFS: License Usage                                             |
+------------------------------------+---------------------+----------+-----------+-----------+---------------+
|                Type                |       Product       | Required | Installed | Available |     Status    |
+------------------------------------+---------------------+----------+-----------+-----------+---------------+
|            User (10.x)             | Emergency Responder |    0     |    100    |    100    | In Compliance |
|      CUWL Professional (11.x)      |      Unified CM     |    0     |    100    |     89    | In Compliance |
|        CUWL Standard (11.x)        |      Unified CM     |    11    |     0     |     0     | In Compliance |
|        Enhanced Plus (11.x)        |      Unified CM     |    13    |     15    |     2     | In Compliance |
|          Enhanced (11.x)           |      Unified CM     |    29    |     60    |     31    | In Compliance |
|            Basic (11.x)            |      Unified CM     |    2     |     4     |     0     | In Compliance |
|      TelePresence Room (11.x)      |      Unified CM     |    4     |     20    |     16    | In Compliance |
|      CUWL Professional (10.x)      |      Unified CM     |    0     |     20    |     20    | In Compliance |
|      TelePresence Room (10.x)      |      Unified CM     |    0     |     5     |     5     | In Compliance |
| CUWL Professional Messaging (11.x) |   Unity Connection  |    0     |    100    |     65    | In Compliance |
|       Basic Messaging (11.x)       |   Unity Connection  |    35    |     0     |     0     | In Compliance |
|     SpeechConnect Port (11.x)      |   Unity Connection  |    0     |     98    |     98    | In Compliance |
| CUWL Professional Messaging (10.x) |   Unity Connection  |    0     |     20    |     20    | In Compliance |
+------------------------------------+---------------------+----------+-----------+-----------+---------------+
```

If you're out of compliance, it'll let you know how.

```
+-------------------------------------------------+
|                   TFS: ISSUES                   |
+---------+-------------------+-------------------+
| Product |      Message      |    Date Raised    |
+---------+-------------------+-------------------+
|   CER   | Application Error | 2020-May-21 00:32 |
+---------+-------------------+-------------------+
```
