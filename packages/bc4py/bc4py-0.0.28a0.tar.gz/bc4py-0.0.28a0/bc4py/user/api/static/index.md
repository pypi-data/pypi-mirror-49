Index page
====
* [sample.md](./sample.md)
* [REST response test](./test-response-rest.html)
* [WebSocket response test](./test-response-ws.html)
* [bootstrap3 components](https://getbootstrap.com/docs/3.3/components/)
* [pyContract 8bit wallet](./8bitwallet.html)

How to close client?
----
Do not kill process or break database file.
* type `curl --basic -u user:password -H "accept: application/json" 127.0.0.1:3000/private/stop`
* access the **[API](./private/stop)** on browser

System
----
[document link](./doc_system.md)

|URL    |Method    |Type    |About   |
|----   |----   |----   |----   |
|[/public/getsysteminfo](./public/getsysteminfo)    |GET    |public   | System public info.                    |
|[/private/getsysteminfo](./private/getsysteminfo)  |GET    |private  | System private info.                   |
|[/public/getchaininfo](./public/getchaininfo)      |GET    |public   | Blockchain info.                       |
|[/private/chainforkinfo](./private/chainforkinfo)    |GET    |public   | chain fork info.          |
|[/public/getnetworkinfo](./public/getnetworkinfo)  |GET    |public   | System network info.                   |
|[/private/createbootstrap](./private/createbootstrap)  |GET    |private   | create bootstrap.dat file.        |
|[/private/resync](./private/resync)                |GET    |private  | Make system resync status.              |
|[/private/stop](./private/stop)                    |GET    |private  | Stop system.                            |

Account
----
[document link](./doc_account.md)

|URL    |Method    |Type    |About   |
|----   |----   |----   |----   |
|[/private/listbalance](./private/listbalance)               |GET    |private  | List all user balance.                 |
|[/private/listtransactions](./private/listtransactions)     |GET    |private  | List user related transaction info.    |
|[/public/listunspents](./public/listunspents)                |GET    |public  | List unused outputs by addresses.      |
|[/private/listunspents](./private/listunspents)              |GET    |private  | List system's unused outputs.         |
|[/private/listaccountaddress](./private/listaccountaddress) |GET    |private  | List user related addresses.          |
|[/private/lockwallet](./private/lockwallet)                  |POST   |private  | delete private key from system        |
|[/private/unlockwallet](./private/unlockwallet)              |POST   |private  | decrypt and recode private key to memory |
|[/private/createwallet](./private/createwallet)              |POST   |private  | generate new wallet private/public pair |
|[/private/importprivatekey](./private/importprivatekey)      |POST   |private  | import private key manually           |
|[/private/move](./private/move)                               |POST   |private  | Move inner account balance.           |
|[/private/movemany](./private/movemany)                       |POST   |private  | Move inner account balances.          |
|[/private/newaddress](./private/newaddress)                   |GET    |private  | Get new incoming address by account.  |
|[/private/getkeypair](./private/getkeypair)                   |GET    |private  | Get keypair by address.               |

Sending
----
[document link](./doc_sending.md)

|URL    |Method    |Type    |About   |
|----   |----   |----   |----   |
|[/public/createrawtx](./public/createrawtx)        |POST   |public   | Create raw transaction by params.   |
|[/private/signrawtx](./private/signrawtx)          |POST   |private  | Sign raw tx by inner keypairs info. |
|[/public/broadcasttx](./public/broadcasttx)        |POST   |public   | Broadcast raw tx.                   |
|[/private/sendfrom](./private/sendfrom)            |POST   |private  | Send to one address.                |
|[/private/sendmany](./private/sendmany)            |POST   |private  | Send to many addresses.             |
|[/private/issueminttx](./private/issueminttx)      |POST   |private  | Issue new mintcoin.                 |
|[/private/changeminttx](./private/changeminttx)    |POST   |private  | Cahge mintcoin's status.            |

Blockchain
----
[document link](./doc_blockchain.md)

|URL    |Method    |Type    |About   |
|----   |----   |----   |----   |
|[/public/getblockbyheight](./public/getblockbyheight)  |GET    |public   | Get block by height.         |
|[/public/getblockbyhash](./public/getblockbyhash)      |GET    |public   | Get block by hash.           |
|[/public/gettxbyhash](./public/gettxbyhash)            |GET    |public   | Get transaction by hash.     |
|[/public/getmintinfo](./public/getmintinfo)            |GET    |public   | Get mintcoin info.           |
|[/public/getminthistory](./public/getminthistory)      |GET    |public   | Get mintcoin history.        |

Others
----
[document link](./doc_others.md)

|URL    |Method    |Type    |About   |
|----   |----   |----   |----   |
|[/](./)                         |GET   |public      | main page                                          |
|[/](./)                         |POST  |JSON-RPC    | Mining interface, `getwork` and `getblocktemplete` |
|[/public/ws](./public/ws)      |GET   |public      | Realtime information stream.                       |
|[/private/ws](./private/ws)    |GET   |private     | Realtime private information stream.               |


API version 0.0.2 2018/11/23
