import streamlit as st
import sqlite3
import hashlib
import random
import pandas as pd
import numpy as np
import plotly.express as px
import requests
VIP_BADGE_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCADIAMgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD4zNFJRQAuaKKKACiiigAozRQBQAUU4LmnCMmrUGwI8GjBqwsRPanCBj/CfyrVYeTFcrYNJg1c+zv/AHD+VNaBh/Cfyp/VpdguVcGjmp2iNMKEVm6TQXI80ZpxWmkVm4tDDNFJS0gCiiigA7UUUlAC0UUUAJS0GkoAWiiigAo60YqREJq4wcgGqtSpGT0FXLDT5rqQJGhOfavYvBvwdkTS4tf8YX8Ph7SHG6OS4UtPcD0hiHzP9ThfevXwmWTra7L+vv8AkY1a0KavJnkFlpdzcMAkZP4V6L4T+C/jPXbZbyHRp4bPqbq6It4QPXe5A/KvY/Df2LT7VX+H3hK1sYAdg8QeINryM3/TNT8gP+yis1W9T0iG8uRc+OPFOoarcHkJcztAn/AYgHmI/wCAIPevYeFweCV60kn57/cv8/kee8dOo3GjG/4/8BfNnntt8IfCmmAf8JD8Q9DgcfeisEkvHHtlQF/WtC28JfB6H5f7T8Waow/59tPijB/76Ymu8sZvB+mgGx0VXx0dbaKIf99zmZ//AB1a1YPFyfct7ZAvYDULhv0iMY/Ss3m+Ep/BBtekV+epPLjJbu3z/wAk/wAzzz/hGfhMF/5AXjzH97ZD/wDE1TufCXwcm+U6l4s0xj3uNPikA/75YGvWP+Elutu77EuPrf8A8/PqtP4tAG25tUKnsb+4X9JTIP0o/t2g9PZv74v8wVLFr7S+9/8AyJ5HP8H/AAhqn/IvfETRJpD92K/SSzc+2WBX9a5XxZ8EPGWh2xu30ma4s8ZF1akTwkf76Ej869yvp/B+pKftmiKhb/lobWKUf99wGF//AB1qr6TpMVhcG58E+KdR0q5HJjtp2nT/AIFEQkwH/AHHvVrGZfX0lo/7yt+KsvwZpGriafxRuvLX8tfwPk3UNHu7RiJYWGPasx4iO1fYet3FpqcBb4ieEbS/ty2w6/oO1JFb/pooGwn/AGXVWrz7xn8FFutOm17wRqEPiDS0G6QwLtntx/01iPzL9Rke9ZYjJ4yV6T/y+T/zs/I7aFeFZe6z54ZSOtN6VvatotzZStHNEVI9RWTLbsnavnq+FnSk4yVmdDi1uV6KGBFAFcghKKWigAFFFFACUtJS0AJSiipI1yauEeZgLGhJrpfB3hfUvEWqW+n6dZzXNxO4SOONcsxPbFHgrw1f+IdZttN0+2kuLieQRxxouSzHtX0po2lw+D7ebwl4PuLc6z5J/t/X8/u7KPo0MTDoM8Fhyx+Va+ly3Lk17Spt/W/kcWKxaoLz/r+vMo+FvDGi+A7mPS9PsLbxT44IyUwJLLTCOpY/dkdepJ+Re+asarNY2F4dZ8T6l/wkWtTjcJZx5kK/9cYzjzAP77bYx2D1k+LvEOmeFLKTw/okWblsfafNUF2bqGuPVu6wfdTgvubgeb6rrU4upfPMl5qUhzIsjMdp9ZWHIP8AsDn129Kyx+d2/d4bTz6v07L+tb3Oejgp1X7Sv93+f/yK+fY9B1fxjfXDPdtdfY4kGxpjMA6r/dMpxsH+wmweimuYPi623mLS7We/kOSXz9nh9yWYF2HvtX61zCWkl9NFNqczzODiNMlUT2RAmB+HPrmux8K+FdT1ib7NpemSvsO6RUXzDx3kbhUUf7R+orw6dGrWldb/ANbs9ByhTjZaJfd92xnPrPim5X5Lm2sA2NgtrVS+PUvLvb6cinxW+oXUix6l4m1OUfIDv1KRRknngMB+ldnLofhTRgT4n8U6as+fmhts30uffaVhB/E06HxV8P7VfLsdK8T6kB0ZDFbIfwSNv513xylrWbS9f6/UweKv8Kb9DgrTRkaVfN1K5wQeTdycnacc7vWpre31GFIpIPEuqwx/MH8vUZW5/hG3cR+nau8/4Tjw23B8Ea6V9f7Xkz+W3+lJN4q8AXY26hpXifTgf4nMV0g/CSNf51o8rhLacfvX+YvrEl9lnDw6x4ktFTfeW2oOz7Sl1ahWx6+ZHsb8yamtvFlvMIxqtncaeW5Rz/pEOQccMoDrz/st9a6+HQPCetsJPDnijTZZc5W3uM2MhPp8xaEn8RXM+LPC2uaPNHbX9tPEVGYVljCMR6qfuuPdT+Fc1XLatLVL7v8AL/gGkMTCbt18zo9K8ZX9uY7mO7+2ROuxJxMGZl/urMM7x/sPvHqorpfD93pl1eLq3h7Uj4d1qH5vOh/dwt7SxjPlg/313RnuErwgW15YNJPpxeGZ2zLkjbJ7PGeD+Iz6EVo6PrsrXUYAey1BDlEVyQx9Y265/wBg8+has8Lja2DfuvTt0+7p/VzSVGFR82z79f8Ag+jPd/EXhfRfiBLJpus2Ft4b8YAfKwAS01AnoR2R27EfK1fOfj/wLqnhnU57K/tJYZImKsrrgg17Z4L8XWOvWkWha0pLL/qGiA3xn+9D755MX3W5K7W4Pf6laaf4y0yLwn4pmtzqZiB0bWc5juk6KjN3B6AnlTwa+rhVo4+jqtvvj6d4+W66aKx34WXP+7rb9H/X4rdeaPhe9tShPFZ7DBr034m+EL7wzrVzYXts8MkTlWVhggivOrqPa5r5nHYOVCbizKtTdOVmVqKXvRXmmQUUlFABRRSjrQA5BWlpVm91cLGoJyapQrk17f8As9+GLFZ7zxhr8Ak0fQ4hcSxt0uJicRQ/8Cbr7A17eV4P209dl/X47GNaqqUHJnd+C9Am8CeHLTTdNiX/AITbxFB8jHg6ZZsOWJ/gd1ySf4UBPeneL9YtfAvh2DRdEffqEyCdZiuGTI4unB/jYE+Sh+4h3kbnGNW3vnsdP1Dxn4hVbrVtWxM8T9GR8mG39lfbvcf88owv/LSvI/FepX811JqFzPJcavqEryLMwyVOTumPpgjag9QT0Su3OsdyL6vD5/5ei/4Ot2efgaDrT9vP5f5/ovv7HN31xPa3LW9oS2obj50xcZtyeoGTzKe5/h/3skTaJYSCRYo7aIsTyBIxxnvgE5JP4n9ag0rRZZUgSCGQu4JdiN2OcZ9zn8/zr028ntPhfp0cNvFHL4wmTdlsEaWpHX/ruRyT/AMAfN93x8Fg/a3nN6Ld/wBf189/Qr1XHRLXoJ/ZOh+CbRJ/F7z3eqOoMWjxSkTHPTz3GfKH/TNfm9dvWsLXPF/iPxHbiyM0el6QhxHYWQEMCfXHVvf5m965gNNc3T3V5K89xKcuzkkknnnvz/d6nqTW1p8DyFSAScYGPT0GO3sMD3revmCguSj7sfxMoULvmnqxLLTYUcZBaTv1DfyZ/wD0GtWC3hLAeXEx/wBoKx/8eZj+lCWkoQAphfTAwfw6fo1WraOUOIyzL/skkfoSP/Qa8x1r63On2bHCzXb/AMeyY/64Jj/0TVWaCFTgRxK3+yFU/wDjrKf0rbTTJWjLbOPXaP8ACs6+glTK5Zh6Ak/oCf5VMa6bsDptGDeWELyElSJOo4Jb88K//oVaGheMvEXh6E2XnR6rpDnEmn3wE0D/AEzwG+m1veoJI3ZSFXK56DGAfp0/RaqzWs2TuVs4wc+noc/yOR711UsZOk/dkZyoqas0dZ/Y/h/xxA114UDW+rRqfM0a4Iebpz5DN/rB/wBM2+b03da811nTG3G3uAVcZwEhwvB68YwfUdRWm1pdW9xHdWbSQXMRzG6ZDKRzx34/u9R1Bru4vJ+JenvFewJH4uhTdwAF1VQPy88DkH+Pofm+96H7rHL3dJ/n/X9d1l79F66x/I830m8me4jtbpn+25AhnI2mc9lb/pp6N/F0PzYJ9x8Aa1beJ9Em0bVpStzGrT+aBllIHNwgHO4ADzUH3lG8fMpz4lfaBKttKZ4VyJkQERKvBzzwMg8fh+VbPgzWb2O9S8juHg1WxkVzKv3mIOFm98n5WHqQf465MFiJYStbb9DtUuaNn/XmvNHs3jLRpviB4YvdK1WJR4y0CEkMDk6haqM7gf4mUYII+8pzXyN4isXs7uSF1IKnvX17Nqkuoabp/i7QAtrquk5mSNOgRCDLB7qm4Oo/55OR/BXln7SPhexkNl4z0GAR6TrcZnSNelvMOJYT/ut09iK+pxdCGLw/NH5fqvTqu2q6IPbOa5J/Ev6+57r7j57cUyrEy4JFQHiviqseVkIBRQKKyGJT0FMqWIZNXBXYGnolq1zeRxgZya+pxpFvpuleG/h9KGjgt4P7d8QlPvElNyx/UR7VA/vSV45+zr4di174h6Xb3Q/0RJfPuSeghjBd/wDx1T+devDU5tRt9b8VuP8AS9d1NvJB7QxFSq/TzHhH0Q19lg7YTBuq97X/AEX6/Ox5GPk6lSNGPX9f8ldmL471c3F9JPeSLHBbM7Slfuq+MykeyhRGvtEo711Xwd0Hwl4u0i01W/0u2jup5JYZJZZJmCBNpiTCuAAI3HPcgnua8i+Kd19ngttFhJ3XDAOT/cTDMT9W2fk1d1+z5qrWQu7SSbfHH5V1GT3AJjfj/dkJ/wCA18FmqqVKM6kXqtf8/wCvI+gwMYxkoJaW/wCGPovw/wDCrRtDuotQ06w0xJ4jviZo5nAb+E4MhHBOR6Hmvmr47eGtPsNcfVbFZYzd7ZXidjIUYqCfmPJ+bd175r628Ba2bgTWFy3+rQNHntzgj9RXzx+0vpjxa5eOoJiQyIAOmNwlT/x2Zh+FeVlONrSrQpSm+WWlr9en4nVUpKXMmtTwK0w0gB78evX+ef1+lfS3wJ8D6Lq3huGfVbOGW4upZDHJKz4VF2qowrAHLb+egxxXzRp//H4oPr9P88fpx3r7e+EOlfZfBFusi7fs8MURPoQnmP8A+PSsPwrrzepKNJKO7Zz4OC1bMzxT4L8J6DAJL20slZ87I1M2+THp+86e/SuI0/SfDh+JL2SWKLaxWTPJbpM4XzliLNznON3v2ra8VX0l1qkup6lIzgtuJY9EXLED22q1eWfD3VZ7vx/cXMzkvJDdM/1MbV52XqVWlVqNuyT+/f8ARnoTgo2T3Z9P2Hw/8PXVgJbezsyjDkt52R9f3lePfG3R/D2maK5sbZFlW7WISKzlWBRj0ctjlevFey6RfzppM8St8rL/AFrwv483J/sjgncLyMjH+5LWGX1ZTxEIvzv+JnKm7Su7h8KtB8OXPhz7brFmtxJJd+WJGZ/3ShT0CsCcn3Neo2vw18Kyor/2RaPG3zKymYgg+h315F8H7l5tCa3JyPtG4f8AfBr15P7RubKztYrieNF3AKjlR19qWY1qlPFSim7GkKceRMsv8J/CM6bBoVqp9d0//wAXVf8A4Un4c+0x3NrYx208bBkeG4mjZSDnIJLDrz0rm18faLYTmG9u9SR0JGHuY1LAMRnDSg4yD2rs/B3xE8O6jcRwWmo3STOwRBOQ0cjf3Q6sy7j2BIJ7VnTxlalJSu9OzM50pW0MT4k/B+HVrKfUoItl07LJPENuZpFVgWQjA3PkZGBzzjtXyb4v0+90fW1voLGZWgYh4vLP7xDw6NjoSMj0zg9q/QKfVYbuzkimRWRhtdD0Ir5T/ae8PCC8Op2qlvNfZcHHLsRuSThTyygg/wC0hPevUw+ZuviPele/c5pUn7PbVGL8PtaaynjktZVmhuCjRl/us2MxsfZgxjb2kYdq6GLSoNW0rxJ4AQM9td2/9t+H9/UMq7mj+pj3KR/ejryT4V3X2hLnSZiwMDHZkEfu3ywxkDowf8xXpzaxPp8OjeJ4v+PvQdTTzh6wykllPt5iTD6OK/RMixUpXovd7eq2+/8AK54mNk4ONWPp9+33PT5ny3r9m1pfSxMMYJrIcV6/+0n4ch0H4iajDaL/AKHJIJ7YjoYpAHT/AMdYflXkcgwTXm5pQVOq+XZ6r0Z1QkpK6IxRR3oryCwFT24y1QDrVq1GXFdGHV5CZ778AYRpngjxp4iAxJBpItIW9HuJAnHvtDV2ltaBDomldFstOjlkHo7gysfzmT/vkVzHgmL7P+z5qRTh9Q161t/qEjdsfmwrc8V6l9j8aa1DE2GDG2Qf7p8sf+ixX1WbS9ng4w7tfgk/zueRSvPGt9k/0X6s8c8eXf8AaHja8JK7bdUiAIyAT85z68vjHfHtXpvwIt7SO31jVtT3JHFAtspc8mS4cRKT9FDtj2ryO8fztb1O8YkH7ZMwJJwMOQOe3AHTJ9K9Ky2nfA6MrmOS+1tI8jj5YYB/WavDyzDwrRmp7cr/AB3/AAuevzuFRNdz6K8Ham8d9YyynbK48qYejfdYf99Cl+KGkWuspqAuuGudLLxH0mj3L+okQfhXFQ6qy6bYaur4XUIEu1IPRzxIPwkV/wA67XxHK+s6Li2b97LbSGEj1eIsv/j6pX5r7+Hq3W8X+KZ9C1ez7nyl4F0ptX8b2GmBf+Pi7jjP0Zhn9Mn8K+9fDNvCngiKMkI9yryntgysWH5KQPwr5L+C2mLJ8Srq/VcR2tpNcp7M67I//HpV/KvoPxb4kXTrTTrWN9oYkgZ/hQBR/M/lXsZ5VXteSPb8/wDhjjo0XZR8ziPjnGNJ0+5gUjPkqP8Av43/AMRG/wD31XkXwojebxS7Dta3Bz/2yau8+POpNNo1hJIx8y+lebB67EAjT/0En/gVYnwKsPO15225/wBEuP8A0U1Thf3OXNfzcz/C36M2nd1F5H0N4dbzNEllBHCf1rw/40I9zoL3B6fbUXj2SWvbPC6vB4X1dJQQ0AI575PFeYfE3Spo/ACPMuHa+V/wKSV5OAq2xEH6/qauOkjM/Z80972MIB/y3I/8hOf6V9F6TpVvbJEZSMq3SvFPgYV0jwuuqsMKb148+/lMP616LN4nT7HBPvH7x2wfoRWuYSU8VOX9bGTjLlSR8m/HW7utP8WqsDsgaANwfWSQ1e+FXiC7ufsmkvbwsL+7S1mmCfvCrnA59Q2GB6ggVu/GPwJr/iXWrTUdG02a7gNnGC8e0gMGfI6+9b/wd8IxeFLT7fr9oBfwyCW2haVSVdQQpIBJ4JBJOOFwMk4r6HEYynLLFTm72jGy7PTb06+VyKcZqu30PUrTWZRp8E07/O1urSH1bbk/rXm3xuvF1XwhqGTxFFFIWx02zKM/lI1aGt6wlrprnfgMBDGCeScf0H8xXH+Mbl3+Hmq3ZUskrQWwY9Mlmf8A9kX86+fy7DupiIRj3/4L/A3qaRbZ4h4Iuk03x3brDLvS4DxN8pGcfOP1TH417bcWatJrWl9RfabJLGPV4wJV/wDRL/8AfVeAWty0HiLTLyRl8z7ZCwAQZwXAJJ6jIJr3TwrqX2zxhoscjZcsLZ/cMfLP/ow19/l9R0sVFruv8j5fGR5sPO3Z/hqvxRy3x+T+1vAngrxCfmkm0o2czer28hTn/gJWvn+cYNfRXjKL7R+zzp5fl9P1+6t/oHjRv5qa+d7ofOa9rPqaUk15/m7fgZ4GV6Vu1yt3ooPWivlWdwLVu0++v1FVF61atThh9a6MM/fQmfSfhUD/AIUTpX93/hK13/8AfgYrP8fSlPiXqIbjOqPn/wACXqz4JlM/7PmoleWsNetbj6B43X+YFZ3xlb7N49vbtfuSzGdT6hiso/SQV9NnsW8NC3f/ANt/4J5WGXLi537P84/5nlIjDXeoSMwDLcS8Y5OXavWPF77fgf4dZen9s3ZP1xb15dfII9b1WMDKrdzbl77S5IYfgRXpN451L4Al15Ona0HI9FmgUg/nCa8vKdYTS7foelNanR+FNTl1P4NIIjm50S/KnP8AzwmXcPydZPzr0Pwx4kY+FdFvEAMtrM0Mq+6MHX8wQK8R+CupbbvVNEkP7q/s2AX1eM7x/wCOhh+Nem+BYikd7p8nOCs6D/aQ7W/MEflXwOd0fZ4lvvr9+/43PocLL2lNF3wZYnw/fa+0eP3t4LaA9/KjZpB+jQ/lTvHl/eX/AMQbLS7UhkgSG3P++fmb9WI/CtrRhDcXUjOhUWZCzk/xOM5P/fCRVzdjM1rfXmvXHMyeZcgn+/yw/wDHto/GvNqV54iqnLeyX3JJfkdCiopswv2gtatLzxpHp9i4a00y2js4yOjFR8x/E10H7Pc0I1abcRj7HcZ/79NXhuuag1xq0js5Y7uvr716N8D9SaLWpArYP2Sf/wBFmvosdh/Z0nTX2Vb7kedSqKVVn054TuLk+FdVN5JbvcpGuTtOBzxu9a8+8eXV5N8N5jqbIZ/7TGCvQr5bYxXSeDZmbwtqytkmZTn35rzD4i6jLH4FEDucreqOv+zJXyWXQlLExXr+p6Mkopv+tjT0y98j4HZtGX7QmrE/QFRVTUteis/CGifa7iZJpPPYiOHd0cD1FUvhZu1bwpPpmdwa48wL7hTUvjrRpYbDT4GU4RJMe2Xrsxvu4twf9aBSinT5jLj8ZWYc7ri6YHv9lH/xVWoPGeiAkzW+p3eAcRpshUn3OSfyFcr418R6R4ZvYLI6BBcs8CytIZihyS3GAMADFcnd/EaBfmstCtYW9Wmkf9AVr1aeS16tNTVkmr7nPLEU4OzZ2Oo3Wo6xqBu7rZZ2kK52k7Uhj9cnoD3Y8k9MnAqfUtbttW+FuvrZBvsNrqVkkJZcF2In3OR2zgYHYAD1ryPW/Fer6yghubjbAGysMahIweBnaOM9eTk+9dnp+7T/AIAPKfv6jrQZR3KwwMx/WYV9XkOWU8M5Tk7yUX6L0/zPOxWL9ouWJ5a6n7dasJIyfPiON4J++texeAZWb4iaeoPTUkx/4EpXk1hFHNrWmoqDJu4VYjcRw4J56HgGvUvg+32nxzZ3TdIplnb6KTKf0jNLDq+Jil3X5nmYh2oTb7P8jS8S4/4ULrPp/wAJWdn/AH5b/wCtXzfdffb6mvojxlL9n/Z6sA/Dajr91cfUJGi/zY187XJyx+tfSZ+9vn+dv0OXLlam/VlY9aKD1or5F7nogOtTwHDCq9SxHBrSi7SA+ivgBINW8AeNPD3WSbShdwr6vbyB+P8AgO6ofiun23QdB1tRkT2MKyH/AGkBgf8A9Fx/99Cuc/Zm8QxaJ8RdNkuz/oksnkXIPQxSAo4/JjXpPinw7LHofiPwfLzc6FqDmE+sExChh7CRYT/wM19jiV9YwDa3sn92j/BL7zzasPZ4mNTo9Pv0/Ox4TqrE6qlwXwJ4I5dw6qyjy3PuMpkj3zXpPwoYav4b8UeFnC77vTzPAi9DLbN5oA+sRkArzTUwW03cwIktHZiO4RwFYfgwX/vo1ufDzX5/D3iqw1W2wZIJ1kCno+0DKn2ZSw/Gvncrq+yq8r9P8v0PRlvcq+D79tF8U2d4x/49rhWceoBww/ED9a+idHVLfWIp0OYxIYmPqvK5/LB/GvEvi7oFvoXjA3Om5fSNRRbywf8AvQyDKj6gZU/7UZr07wdrEMvhW2vbiVCz267Qzhd8ifu26+yxt/wKvB4qwbjFTXR2+T1R62WPeDPRbuBYrS6Fum17g/OR3YgKT/3yorz74nXP9maBNErbXbarf+hEfpF+dbnhvxVP9rEerz2L27nG9CqmM+p55Fed/HXVQ9vaIrgm7L3RAPRWOEH/AHyF/Kvmskw8p46HNtHX7tfz0PTxbjCi2jyqSctOz5716B8Hb3b4gck8fZJ//QDXmYJruPhAwPiCUMQB9juD/wCQzX1eIjzUqjf8svyZ4GGbdVH1h4al8vSLlAeCP/Zq8h+NU3kaG8I6i6jbH1WWunn8YPYultYm1lgz++LOMyD0Bz8uPXufauI+Nt3b3mhNeW8qurXEA4IOD5cvBx3r4/JYP67C/W/5M97FR5aUmWvgxqJsdL+0MSAZSAf+A16pq0lprcFs0rBXCFR7814r4CZV8DQTF1QG7kUktjooPeulsvEdw0sMUr2sdtDxHh13deSxzz/Srzmk3jJyj0/yHhLeyVzzH42sD4gjPpAB+TuK87OO/Tv9P/1fzrvPjLL5ms27ghle3VgQeCC71wG7vkfX9f8A6/0Ar7DDL9xT/wAK/I+exelZksaNJKsa/fY4H1PH8yfyr1L4ssmj+E/DHhcDDWunfarlM4PmXJ8zB9xEsYrn/g34dg1zxWlxqOY9I05GvNQkP8EMYyw+pGFH+1IKzviT4gm8ReKNQ1ecBWuJHkKDomcbVHsq7VFe/RX1fCOT3l/X+f4HPbS5h6OSdZF0AN1vA8pOOFJXYgHoMuPyr1P4XKLLQde1tvl8ixmWM/7TgQL+ssn/AHya8u0oFNPMm0mS7cEDuUTKr+blv++RXt2haBM+g+HfB8HF1r+oJ5pHaCIlSx9jI0x+iCsclpe1xak9lr8kcWYzUaHL30/V/gmc/wDHuX+y/A3grw7nbJDpRvZl9HuJC4z/AMBC14DOea9U/aN8RQ698RNUuLQ/6HHL9ntQOghiARP0UfnXlEhya688q81RRfT83q/xZphIOFKKZH3oo70V84zqEp6GmUo6007MDc8NXzWWpQzK2NrCvrXUNUttR0rw38RHBltLu3/sTxCq9fu7Q59ymGB/vR18awPtYEV9C/s3+KrC6ivfBGvzBNK1qMQM7dIJhzHKP91v0Jr63JsSpQdN9PxXVfdqvNIzq0lVpuDOX+JOhS+H/FdzFPGJYpWdZNn3ZAR8+PZlYOPZx6VwriSzuTA0mWRtySD+JSAVYfUY/HIr6D8Y6BdX+jXvh/VE8vX/AA2DHJu/5a2qn5JR6+Xuwf8Apm4P8FeKazpUsiBfLZZ4GIVe/X5o/wA+R7/71eHj8K8JXdtunoTQqe1hrut/X/g7o9C8JyQ+PvBB8HzY/tezLz6K2eZCfmltR7nG9P8Aayv8VcJa+IfEOgxvp9tf3NsiSFjGrYUMeM4PTOB+WKy9B1F7G6jubeSWN0YNkSKrKQcgjnIYHpXqutadafFHTG1jSVjXxVFGXvrWNeNQUD5p4lHV+MyRjnOXX+IV6MJrG0v7y/H+v68umDf2dzi4PF3jqW1ku4LrVpbVPvzRxM0a/VguB+PSszV4vE+pXwfUNP1ea5mBYeZaSl3AwCQCuSBx04HFaWmeMNc8PaVb6RZxpCbaSdzJIzE4m2hsAMF6AjcQ3Xtitf8A4WjftJPvsXSOd7l5RHcFt3mvGwJ8zdyPLwcYU5zgGvnq9XFQk48n5I05lJe9I4R7O8jnEElncpKQSI2hYN8uc8EZ4wc+mDV/Rr3W9H1BZdMW8t7wA7THGwkAPynjGcHOP0rqbX4ha/b6eq2FrPJp1nFNBLLKA8kYuXlJXzgv7sOXAKj73lgDvWrJq3ihNd/4SU+C/EYuogLRmw4jAF0Jdp/d7g+4hcZ6kfSuf6xVg/hX3ijGKd1I5wfELxuke7+29TCF/LB8w43D+H6+3Wota1Lx1rCJa6nBrt0vMixy20pPpuA2++M+9acmu+NvEraeP7Evb6TTtYa9AtrMqrToFMoYKvMpOGdjzyMgcVas9Q8U2P8AassPhjxReRzuIrr+0pp5EiKSiQplApU8gdeMg4NVLFVEvhV/l/wC+dvRyOY0nXfFWmZsNMl1CDfiQwxI2Wx8u7bj8M/hWkPEPxEMjRbde8xQCyfZJNwz04255wcfStDU/FPjLRbxZdb0rU7F5NY/tJDcxGGR41k8wwBioOzzNrkZxu5xmsZfHuvyK0b3UkCfYZ7WJLWaSML5pyXJLEsQeeuB2xVxxFeWqin9zFz8unMZev3Gv6gkeoazFfujAJHcXELhSBnChiMHvwKzrO2mu7pLeFdzscAdfrn6d/wFdRe+J7zWtMl0pY9QlmuoLSFg97vgUW4UB0Qj5c7RlieMnrXbaLp9p8LNKXWNTWOTxXNEJLG1kXiwU/duJVPRucxxnnOHYfdFepgMPOv79VWijNw5pXuQ+L3g+H/ggeD4D/xN7zZPrR7x4+aK1PuCfMk/2sL/AA15JIj3d0LZXIMjPvf+4uAWY/QZ/HAqfW9Sl1G6lvLqWVwzkksdzyMTk892J5J/ydHRdMnVSZIibm4YBkHbn5Yx+OCffH92jH4r20+WGy/q5DfM/I3vh7oU+v8Aie2htkEUcTIse/7seB8mfZVUu3sh9a9YttYt9L0zxL8QIgY7WztxoPhwP1LFNpkHuI9zE/3pKx/DeiXenaRZ6FpCebr3iQeTDt/5ZWzkb5T6CTbtB/55oT/HXJftCeJ9PWSy8GaBOJNI0KM28ci9LmY8zTf8Cbp7AV9BlmHWDwzqTWr/ACXT57el+x41WX1vE8q+GP8AT/FWXo+55Brd0bi8kcnPNZLmppmyagPWvmMXWdWo5PqeukAooFFcYwooooAch5rW0PUZbC7jnicqykHisfpUkb4NdeFrypTUovYNnc+vPCmvyfELw3Z6xpcqr448Ow5VcZOo2ijlSP4nVcgj+JMiuQ8WaTY31sPEei2+3T5mEVzajlrOYj/VHvtODsb+Jfl+8vPj/gTxPf8Ah3WLbUNPupLeeCQPHIhwVIr6O0/Urfxha3Hi3wha239seSR4g8PlcxX0XV5Y0HUHqyjlT8y19a40swodn+T/AMn+G21jzcVzUZ+2ht1X9fg+noeCa9pDLMbuwJd25ZFx+99xkH5v5/XrBoWr3VldRXdlcSxzRuHR0dlZGB6qQoww9a9M8TeG7a+06XXvDMjz2Q5ureUgzWbH+GX1XPSXoejbW5Pm2q6fBcXD/aVe2u1PzSFTz7SL1P8AvDn/AHq+Wq0q2Bq2ejR20a0K0eeL/rz7M9Ia/wDC/wAQ4QuvSQ6H4hPTUhGUt7lj3nVRmJz3kUFW6sv8VcT4w8C+IfDFysd/YuIpPmgnjw8Uy/3kZSVYe6k+4rnds+nTR+dE8Zf/AFUiOWV/91gMH6dfUV2nhL4g674egeyguUmspTmayuIhNbv/AL0T5XPbcuD9K9COKw+Ljaro+/8AX9eh0pxektzn/D/iPVvD1rewaXKYHu2iMrgBuE34BUgg8vkZHBVSORWxe/ES+v5oJryzEs9vdC5SQ3ILFhIJOSUL8sOcMM5rqhrfwz8RYGr+HrnSbpusulTB4/r5M3zD6K9K/gf4fXg3WHj6C3z0TULGeEj8hIv61zTyKnVlzQaf5/gbwpzatCVzlrX4k68kUkV+W1BX8z/WMFwHChuCjKzEqCzMCWPJ5o1L4gz6iv8ApOnIZEuBPEwuFBVh5eP+WZb/AJZL90qPaum/4Vh4b+9/wsPwvj/rtJn8vJzUsXgb4f2fN/4+hnx/BYWM8xP5iMfrUf6uWd2rfeaeyrpannviXxJf+Io4Ibq0trcx3M9wBbxiNXeUgklQOWAUDdjkAcA8m94N8A+IvE9y0djYyeXGN080gCxxL/edmIVR7uR9K7dtc+F3hpT/AGV4futWul6S6pOIo8/9cofmP0Z65jxj8Stf8QwDT3lEGnw8x2dtEsNvH6FYlwCfc5NdVPBYTCR9+V/Jf1/kZShFO85XfkdR/aHhb4c2xTQpINc8QjrqRTfbWzDvCrDM0g7OwCr/AAr3ryrxBrN3qd1LdX5upnkkLs7uSzsT95iQSWOf8KrxLe6nLIYkaUpxLNISiRj/AGmzgfTr6A1q6VZQWs6fZ/Mu7xuBKA3B9I1PI/3j83+7XLiswlW/d01Zf1uYyk5eSF0DRmMwvL/ETp/q4u0I9/8Aa/l/vdPSPDGmWFlZP4g1q3P2CBjFb2x+VryXH+qHcDpvb+Ffl+83EXh3w7b6fp0Ov+JZHgsjza28JHm3bD+GL2zwZfur0Xc3TsNVvrbwfZW/jDxfa239smEf8I94e2/urKLqksqHoo6qp5Y/M1ellWV3tWrLTou/+SX9efkYvFOT9jR36v8ARefd9PUp+MNfuPAXh291LVJVbxx4jhOVAwdMs2HAA/gd1wAP4Ux618y6pdvc3DSM2STWv418S6h4i1m51HULqS4nuJDJJI5yWY9TXMyNk082x6m/Zwen9fgun+dzpwuHVCFuo1jTKU9aK+abudQCigUUgA0lLRQAlKDRRQgJopCprqPB3inUvD2qW+o6ddy21xA4eOWNsMprkQcVJG5U16GExs6ErxZMopqzPqrwx4k0bx7dx6rpuo23hXxuo5fIjstSJ6hh0jdu4PyN3xVLxLomlapqD6R4g0weFNfj4MUoMdrKfWN+fKz6HdGexWvnKw1Ga2kDRuR+NexeDPjC7aVD4f8AGGnweItIQbY47pis9uPWGYfMn05HtX09PE4bHQ5Ki/ryf6P5NbHlVMHUpS56D/r9V5P5FDxD4L8R+H53hW2a4jkG5oDGGMq+vlnKyD/aQsPcVyJt9KllYSLc6XMOD5QM0Q9jGxDr+DH6V9BeHIrHUbXyvAHi60vLZzvPhzxEEVg3pGzfu2P+0pRqr+J7DSvNFr438Hajolx0EktubmE+6sSsoH0kYe1eVisgnzXoO/ls/u6/l5mtLMmvdrRs/L/LdfK54P8A2Rfyny9NvtM1BWwdsdysch/4BLsP5ZpzaP4os+X0PWY+WJZbWQrjtyoIr1SX4Y+DdVGdI8RRozdES8Q/+Q7gRt/4+ahX4IeILc79K8QzRjsVsbgf+PQGQfrXk1MJjKLtKLXyf6HZHGYaW00vnb8HZnlaHXgWVrPWN+PlAt5c5/KrMWg+Lb+HMXh/X5nz942koTHuWAH616ivwn+I33f+E1uVX0zqn8vKof4G67c/Pq/imeYdydPuX/Wcxj9ajlxctLP7pFPE0FvNfev8zyxvD9/EzLqt/pWlfIFKz3iySdv+WcO9u3fFMFvokEqrFHdaxMcKpmBghP0jUl3/ABZfpXrsHwt8C6QudU18zsvVJLyNB/37thK35utdJ4Y07TDJ9l8DeDb/AFacjBkhgNtEP958tKR9ZEHtXXRyfGVtZKy7vRf5mcsZSSvH3vRX/F2j+J5doPgrxP4hljhltmtYohuS3WIKYl9REMLGP9pyo9Sa7nwzoWlWF4mj+HtLHinxBLwIogZLaM+sr8ebj+6u2Mdy9dD4itLDSLUp8QvF1pZWyHePDvh/azMfRyPkU/7TFmrzTxt8ZCmlzaB4M06Hw5o8g2yR2zFp7kf9Npj8zfTge1e7hstw2ESnUfM/uj8lu/lp5o5JvE4nRe6v66/5fedr4l8RaL4Au5dU1XULXxX43I+VsiSy0wjoB2kdewA2LjvXz14y8Uan4j1a41HUrya5uJ3LySSNlnNZOo6jNdOWkcnPas93JrkzDNudONPb8/8AJeX6nTQw0KK03FkfNRE5oJzRXzk5uTOoKSloqACikooAKKKKACilooASloooAcrVIkpHeoKXOK1hVcQsbFhq91akeXKeO1emeDfjh4w0G3W0j1Waaz6G2ucTQkf7j5FeOBqeHPrXp0M0qwXLe67PVEuKejVz6Ws/jH4K1YD/AISP4f6LLIfvS2Je0c++FO39K17HxL8ELk7jZeJdLY/88L1JAPzUGvlUSn1p63Djo7D8a9Onntlqvub/ACvb8BqFJbx/M+v49c+CgTnxJ4xI/u7k/wAap3nir4FWvziy8Samw/57XSID+QJr5O+1y/8APR/zpGuZD1dvzrR55Hs//Av8kjVOjH4YI+mr/wCNXgbSB/xTXw+0iOQfdmv3a5Ye+DgfpXCeM/jz4016BrRtVkt7M8C2tQIYgPTamBXjjSk96YXPrXFVzmTd4qz77v73dkykm7pf18zV1DV7u8ctNMzZ96zXlJNQlqTOa8mti6lV3k7k7jmam0UVyOTYCUUtApAFJS0UAFFAooAMUYoooAMUc0UUAGKMUUUAGKMUUUAGKMUUUAHNGTRRTuAuTSc0UUXYBzRg0UUrgGKMUUUAGKKKKADFdndWnw2ea1W01XX4oza4uWnt0ZlnDYLIFxlSOQpPHQsT1KKAK8lj4CWKQx65rMkikhFNiqhxgnOdxxk4HerI074bszH/AISHXVU8qrWCkjI6Eg9Qe47D34KKAM7V7HwhDpUsmma5qN1fB18qOSxEaMvO7J3HB6Ede47AkoooA//Z"

from datetime import datetime, timedelta

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None


# Configuración de página de Streamlit
st.set_page_config(
    page_title="Alianza CryptoWallet v31",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

if st_autorefresh is not None:
    st_autorefresh(interval=10000, key="datarefresh") # Auto-refresh every 10 seconds


# --- BASE DE DATOS Y CONFIGURACIÓN ---

def init_db():
    conn = sqlite3.connect("wallet_pro.db")
    cursor = conn.cursor()
    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            fullname TEXT,
            email TEXT,
            wallet_code TEXT UNIQUE,
            balance REAL DEFAULT 0.0,
            is_admin INTEGER DEFAULT 0,
            balance_cop REAL DEFAULT 0.0,
            is_vip INTEGER DEFAULT 0,
            nequi_number TEXT DEFAULT '',
            referred_by TEXT
        )
    """)
    # Tabla de transacciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_code TEXT,
            receiver_code TEXT,
            amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Tabla de configuraciones del token personalizado
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS token_settings (
            id INTEGER PRIMARY KEY DEFAULT 1,
            token_name TEXT DEFAULT 'SIAD',
            token_symbol TEXT DEFAULT 'SD',
            token_contract TEXT DEFAULT '0xC324649213ec1757190bc4b78bcD41Cc1545C264',
            token_price_usd REAL DEFAULT 0.50,
            nequi_number TEXT DEFAULT '3001234567'
        )
    """)
    # Tabla de solicitudes de compra (Comprobantes)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT,
            amount_cop REAL,
            amount_sd REAL,
            proof_image BLOB,
            status TEXT DEFAULT 'PENDING',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Tabla de comisiones por referidos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS referral_rewards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_code TEXT,
            referred_code TEXT,
            purchase_id INTEGER,
            purchase_amount_sd REAL,
            reward_amount_sd REAL,
            status TEXT DEFAULT 'PENDING',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Tabla de solicitudes de retiro (Withdrawals)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS withdrawal_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT,
            amount_cop REAL,
            fee_cop REAL,
            net_cop REAL,
            nequi_number TEXT,
            receipt_image BLOB,
            status TEXT DEFAULT 'PENDING',
            fee_status TEXT DEFAULT 'UNCLAIMED',
            approved_at DATETIME,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla de notificaciones del usuario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT,
            message TEXT,
            status TEXT DEFAULT 'UNREAD',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla de pagos de móviles (Mensajería)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movil_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT,
            payment_type TEXT,
            amount_sd REAL,
            amount_cop REAL,
            target_code TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla de artículos de la tienda (Store)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS store_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price_sd REAL,
            item_type TEXT
        )
    """)
    
    # Tabla de compras en la tienda
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS store_purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT,
            item_id INTEGER,
            price_sd REAL,
            status TEXT DEFAULT 'PENDING',
            code_delivered TEXT DEFAULT '',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(item_id) REFERENCES store_items(id)
        )
    """)
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN balance_cop REAL DEFAULT 0.0")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN referred_by TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN is_vip INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE movil_payments ADD COLUMN message TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN nequi_number TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS store_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                price_sd REAL,
                item_type TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS store_purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_code TEXT,
                item_id INTEGER,
                price_sd REAL,
                status TEXT DEFAULT 'PENDING',
                code_delivered TEXT DEFAULT '',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(item_id) REFERENCES store_items(id)
            )
        """)
    except Exception:
        pass

    try:
        cursor.execute("ALTER TABLE withdrawal_requests ADD COLUMN approved_at DATETIME")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE withdrawal_requests ADD COLUMN fee_status TEXT DEFAULT 'UNCLAIMED'")
    except sqlite3.OperationalError:
        pass

    # Migraciones inteligentes en caso de que ya existan las tablas sin las nuevas columnas o tablas
    try:
        cursor.execute("ALTER TABLE token_settings ADD COLUMN nequi_number TEXT DEFAULT '3001234567'")
    except sqlite3.OperationalError:
        pass 
        
    try:
        
        cursor.execute("UPDATE token_settings SET token_name = 'SIAD', token_symbol = 'SD', token_contract = '0xC324649213ec1757190bc4b78bcD41Cc1545C264' WHERE id = 1")

    except Exception:
        pass

    # Insertar artículos de la tienda por defecto si está vacía
    try:
        cursor.execute("SELECT COUNT(*) FROM store_items")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO store_items (name, description, price_sd, item_type) VALUES 
                ('Membresía VIP Alianza', '🔒 Reduce comisión de retiros a Nequi al 1% y aumenta tu bono de referidos al 25% de por vida.', 50.0, 'MEMBERSHIP'),
                ('Netflix Premium (1 Mes)', '🎬 Pin digital para canjear 1 mes de Netflix Premium en cualquier cuenta.', 30.0, 'GIFT_CARD'),
                ('Spotify Premium (1 Mes)', '🎵 Código oficial de 1 mes de Spotify Premium para tu cuenta.', 15.0, 'GIFT_CARD'),
                ('Free Fire (100 Diamantes)', '🔥 Recarga inmediata de 100 diamantes de Free Fire usando tu ID de jugador.', 8.0, 'GIFT_CARD'),
                ('Roblox (400 Robux)', '🎮 Código de tarjeta de regalo digital de Roblox de 400 Robux.', 12.0, 'GIFT_CARD')
            """)
    except Exception:
        pass

    # Insertar configuración por defecto si está vacía
    cursor.execute("SELECT COUNT(*) FROM token_settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO token_settings (id, token_name, token_symbol, token_contract, token_price_usd, nequi_number)
            VALUES (1, 'SIAD', 'SD', '0xC324649213ec1757190bc4b78bcD41Cc1545C264', 0.50, '3001234567')
        """)
    
    # Crear un administrador por defecto si no existe
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_pw = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("""
            INSERT INTO users (username, password, fullname, email, wallet_code, balance, is_admin)
            VALUES ('admin', ?, 'Propietario de la App', 'admin@cryptowallet.com', '99999', 10000000.0, 1)
        """, (hashed_pw,))
    conn.commit()
    conn.close()

init_db()

# Funciones auxiliares de base de datos
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    return sqlite3.connect("wallet_pro.db")

def generate_unique_wallet_code():
    conn = get_db_connection()
    cursor = conn.cursor()
    while True:
        code = str(random.randint(10000, 99999))
        cursor.execute("SELECT 1 FROM users WHERE wallet_code = ?", (code,))
        if not cursor.fetchone():
            conn.close()
            return code

def get_token_settings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT token_name, token_symbol, token_contract, token_price_usd, nequi_number FROM token_settings WHERE id = 1")
    settings = cursor.fetchone()
    conn.close()
    if settings:
        return {
            "name": settings[0],
            "symbol": settings[1],
            "contract": settings[2],
            "price_usd": settings[3],
            "nequi_number": settings[4]
        }
    return {
        "name": "SIAD",
        "symbol": "SD",
        "contract": "0xC324649213ec1757190bc4b78bcD41Cc1545C264",
        "price_usd": 0.50,
        "nequi_number": "3001234567"
    }

def update_token_settings(name, symbol, contract, price_usd, nequi_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE token_settings 
        SET token_name = ?, token_symbol = ?, token_contract = ?, token_price_usd = ?, nequi_number = ?
        WHERE id = 1
    """, (name, symbol, contract, price_usd, nequi_number))
    conn.commit()
    conn.close()

def update_store_item_price(item_id, price_sd, name, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE store_items 
        SET price_sd = ?, name = ?, description = ? 
        WHERE id = ?
    """, (price_sd, name, description, item_id))
    conn.commit()
    conn.close()
    return True

# Gestión de solicitudes de compra
def submit_purchase_request(user_code, amount_cop, amount_sd, image_bytes):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO purchase_requests (user_code, amount_cop, amount_sd, proof_image, status)
        VALUES (?, ?, ?, ?, 'PENDING')
    """, (user_code, amount_cop, amount_sd, image_bytes))
    conn.commit()
    conn.close()

def get_pending_purchases():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.user_code, p.amount_cop, p.amount_sd, p.proof_image, p.timestamp, u.fullname, u.username
        FROM purchase_requests p
        JOIN users u ON p.user_code = u.wallet_code
        WHERE p.status = 'PENDING'
        ORDER BY p.timestamp ASC
    """, conn)
    conn.close()
    return df

# Gestión de Comisiones por Referidos
def get_pending_referral_rewards():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT r.id, r.referrer_code, r.referred_code, r.purchase_amount_sd, r.reward_amount_sd, r.timestamp,
               u1.fullname as referrer_name, u2.fullname as referred_name
        FROM referral_rewards r
        JOIN users u1 ON r.referrer_code = u1.wallet_code
        JOIN users u2 ON r.referred_code = u2.wallet_code
        WHERE r.status = 'PENDING'
        ORDER BY r.timestamp ASC
    """, conn)
    conn.close()
    return df

def approve_referral_reward(reward_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT referrer_code, reward_amount_sd, referred_code FROM referral_rewards WHERE id = ?", (reward_id,))
    res = cursor.fetchone()
    if res:
        referrer_code, reward_amount_sd, referred_code = res
        cursor.execute("UPDATE referral_rewards SET status = 'APPROVED' WHERE id = ?", (reward_id,))
        conn.commit()
        conn.close()
        
        # Enviar comisiones desde la billetera maestra (99999)
        success, msg = send_points("99999", referrer_code, reward_amount_sd)
        if success:
            # Obtener nombre del referido
            conn2 = get_db_connection()
            cursor2 = conn2.cursor()
            cursor2.execute("SELECT fullname FROM users WHERE wallet_code = ?", (referred_code,))
            ref_user = cursor2.fetchone()
            referred_name = ref_user[0] if ref_user else "Tu referido"
            conn2.close()
            
            add_notification(
                referrer_code,
                f"💰 <b>¡Comisión de Referido Recibida!</b> El administrador ha liberado tu comisión de "
                f"<b>{format_num(reward_amount_sd)} SD</b> por la compra de tu referido <b>{referred_name}</b>. ¡Gracias por expandir nuestra comunidad!"
            )
            
            # Enviar notificación al admin de que ya la pagó
            add_notification(
                "99999",
                f"👥 <b>Comisión Pagada:</b> Se han transferido con éxito <b>{format_num(reward_amount_sd)} SD</b> de comisión al referidor <b>{referrer_code}</b>."
            )
        return success, msg
    conn.close()
    return False, "No se encontró el registro de la comisión."

def reject_referral_reward(reward_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE referral_rewards SET status = 'REJECTED' WHERE id = ?", (reward_id,))
    conn.commit()
    conn.close()
    return True

# Sistema de Notificaciones
def add_notification(user_code, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notifications (user_code, message) VALUES (?, ?)", (user_code, message))
    conn.commit()
    conn.close()

def broadcast_notification(message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT wallet_code FROM users WHERE is_admin = 0")
    users = cursor.fetchall()
    for user in users:
        user_code = user[0]
        cursor.execute("INSERT INTO notifications (user_code, message) VALUES (?, ?)", (user_code, message))
    conn.commit()
    conn.close()


def get_unread_notifications_count(user_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM notifications WHERE user_code = ? AND status = 'UNREAD'", (user_code,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_user_notifications(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT id, message, status, timestamp 
        FROM notifications 
        WHERE user_code = ? 
        ORDER BY timestamp DESC
    """, conn, params=(user_code,))
    conn.close()
    return df

def mark_notifications_as_read(user_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET status = 'READ' WHERE user_code = ?", (user_code,))
    conn.commit()
    conn.close()

# --- FUNCIONES DE LA TIENDA Alianza ---

def get_user_purchases(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT id, amount_cop, amount_sd, proof_image, status, timestamp as Fecha
        FROM purchase_requests
        WHERE user_code = ?
        ORDER BY timestamp DESC
    """, conn, params=(user_code,))
    conn.close()
    return df

def buy_store_item(user_code, item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Obtener precio y tipo del artículo
    cursor.execute("SELECT name, price_sd, item_type FROM store_items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    if not item:
        conn.close()
        return False, "El artículo seleccionado no existe."
    
    item_name, price_sd, item_type = item
    
    # 2. Verificar si ya es VIP si intenta comprar membresía VIP
    if item_type == 'MEMBERSHIP':
        cursor.execute("SELECT is_vip FROM users WHERE wallet_code = ?", (user_code,))
        user_vip = cursor.fetchone()
        if user_vip and user_vip[0] == 1:
            conn.close()
            return False, "Ya eres un miembro VIP de Alianza."
            
    # 3. Verificar saldo del usuario
    cursor.execute("SELECT balance FROM users WHERE wallet_code = ?", (user_code,))
    balance_row = cursor.fetchone()
    if not balance_row or balance_row[0] < price_sd:
        conn.close()
        return False, "Saldo de tokens SIAD (SD) insuficiente para realizar esta compra."
        
    try:
        # 4. Descontar balance de SD del usuario
        cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (price_sd, user_code))
        
        # 5. Registrar la compra en store_purchases
        cursor.execute("""
            INSERT INTO store_purchases (user_code, item_id, price_sd, status)
            VALUES (?, ?, ?, 'PENDING')
        """, (user_code, item_id, price_sd))
        purchase_id = cursor.lastrowid
        
        # 6. Registrar una transacción ficticia para el historial de transacciones
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES (?, 'SYSTEM_STORE', ?)
        """, (user_code, price_sd))
        
        conn.commit()
        conn.close()
        
        # 7. Notificación al usuario
        add_notification(
            user_code,
            f"🛍️ <b>¡Pedido recibido!</b> Has comprado <b>{item_name}</b> por <b>{format_num(price_sd)} SD</b>. "
            f"Tu pedido se encuentra pendiente de entrega por el administrador."
        )
        return True, "Compra registrada con éxito. Se encuentra en espera de entrega por el administrador."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar la compra: {str(e)}"

def deliver_store_purchase(purchase_id, code_delivered=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.user_code, p.item_id, p.price_sd, i.name, i.item_type 
        FROM store_purchases p 
        JOIN store_items i ON p.item_id = i.id 
        WHERE p.id = ? AND p.status = 'PENDING'
    """, (purchase_id,))
    purchase = cursor.fetchone()
    
    if purchase:
        user_code, item_id, price_sd, item_name, item_type = purchase
        try:
            # Si el artículo es membresía VIP, activar VIP en el usuario de inmediato
            if item_type == 'MEMBERSHIP':
                cursor.execute("UPDATE users SET is_vip = 1 WHERE wallet_code = ?", (user_code,))
                # ¡Devolver el valor de la membresía en tokens SD como cashback / reembolso de bienvenida!
                cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (price_sd, user_code))
                # Registrar el reembolso en la tabla de transacciones
                cursor.execute("""
                    INSERT INTO transactions (sender_code, receiver_code, amount)
                    VALUES ('SYSTEM_STORE_REFUND', ?, ?)
                """, (user_code, price_sd))
                msg_notif = f"👑 <b>¡Membresía VIP Activada!</b> El administrador aprobó tu membresía VIP de Alianza. " \
                            f"Por ser un beneficio VIP de bienvenida, te hemos reembolsado el 100% de su valor: <b>{format_num(price_sd)} SD</b> ($30.00 USD) de inmediato a tu cuenta. " \
                            f"Ahora tus comisiones de retiro se reducen al 1% y tus ganancias de referidos aumentan al 25% de por vida. ¡Disfruta tus privilegios!"
            else:
                msg_notif = f"🎁 <b>¡Tu pedido ha sido entregado!</b> Has recibido tu <b>{item_name}</b>. "                             f"<b>Código/Pin de Activación:</b> <code style='font-size:1.1rem; color:#ffd700;'>{code_delivered}</code>. ¡Gracias por usar la tienda Alianza!"
            
            # Actualizar estado de la compra
            cursor.execute("UPDATE store_purchases SET status = 'DELIVERED', code_delivered = ? WHERE id = ?", (code_delivered, purchase_id))
            conn.commit()
            conn.close()
            
            # Notificar al usuario
            add_notification(user_code, msg_notif)
            return True, "Pedido entregado con éxito."
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, f"Error al procesar la entrega: {str(e)}"
    conn.close()
    return False, "No se encontró el pedido o ya fue procesado."

def reject_store_purchase(purchase_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.user_code, p.price_sd, i.name 
        FROM store_purchases p 
        JOIN store_items i ON p.item_id = i.id 
        WHERE p.id = ? AND p.status = 'PENDING'
    """, (purchase_id,))
    purchase = cursor.fetchone()
    
    if purchase:
        user_code, price_sd, item_name = purchase
        try:
            # Reembolsar los tokens SD al usuario
            cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (price_sd, user_code))
            
            # Revertir la transacción de la tabla de transacciones
            cursor.execute("DELETE FROM transactions WHERE sender_code = ? AND receiver_code = 'SYSTEM_STORE' AND amount = ? ORDER BY timestamp DESC LIMIT 1", (user_code, price_sd))
            
            # Actualizar estado a REJECTED
            cursor.execute("UPDATE store_purchases SET status = 'REJECTED' WHERE id = ?", (purchase_id,))
            conn.commit()
            conn.close()
            
            # Notificar al usuario
            add_notification(
                user_code,
                f"🔴 <b>Pedido Cancelado:</b> Tu compra de <b>{item_name}</b> fue rechazada y reembolsada. "
                f"Se han devuelto <b>{format_num(price_sd)} SD</b> intactos a tu billetera."
            )
            return True
        except Exception as e:
            conn.rollback()
            conn.close()
            return False
    conn.close()
    return False

def get_pending_store_purchases():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.user_code, p.item_id, p.price_sd, p.timestamp, i.name, i.item_type, u.fullname, u.username
        FROM store_purchases p
        JOIN store_items i ON p.item_id = i.id
        JOIN users u ON p.user_code = u.wallet_code
        WHERE p.status = 'PENDING'
        ORDER BY p.timestamp ASC
    """, conn)
    conn.close()
    return df

def get_user_store_purchases(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.price_sd, p.status, p.code_delivered, p.timestamp, i.name, i.item_type
        FROM store_purchases p
        JOIN store_items i ON p.item_id = i.id
        WHERE p.user_code = ?
        ORDER BY p.timestamp DESC
    """, conn, params=(user_code,))
    conn.close()
    return df

def approve_purchase(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.user_code, p.amount_sd, p.amount_cop, u.fullname, u.referred_by 
        FROM purchase_requests p 
        JOIN users u ON p.user_code = u.wallet_code 
        WHERE p.id = ?
    """, (request_id,))
    req = cursor.fetchone()
    if req:
        user_code, amount_sd, amount_cop, fullname, referred_by = req
        # Actualizar estado de la solicitud
        cursor.execute("UPDATE purchase_requests SET status = 'APPROVED' WHERE id = ?", (request_id,))
        conn.commit()
        conn.close()
        
        # Enviar los tokens desde la billetera maestra (99999) al comprador
        success, msg = send_points("99999", user_code, amount_sd)
        if success:
            # Enviar notificación oficial de aprobación al comprador
            add_notification(
                user_code, 
                f"🟢 <b>¡Compra aprobada con éxito!</b> El administrador validó tu transferencia de <b>${amount_cop:,.0f} COP</b>. "
                f"Se han acreditado <b>{format_num(amount_sd)} SD</b> directamente a tu billetera."
            )
            
            # Si tiene un referidor válido, calcular el 20% (o 25% si es VIP) y crear registro de comisión pendiente
            if referred_by:
                conn2 = get_db_connection()
                cursor2 = conn2.cursor()
                cursor2.execute("SELECT is_vip FROM users WHERE wallet_code = ?", (referred_by,))
                ref_vip_row = cursor2.fetchone()
                is_ref_vip = ref_vip_row[0] if ref_vip_row else 0
                ref_pct = 0.25 if is_ref_vip == 1 else 0.20
                reward_amount_sd = amount_sd * ref_pct
                conn2 = get_db_connection()
                cursor2 = conn2.cursor()
                cursor2.execute("""
                    INSERT INTO referral_rewards (referrer_code, referred_code, purchase_id, purchase_amount_sd, reward_amount_sd, status)
                    VALUES (?, ?, ?, ?, ?, 'PENDING')
                """, (referred_by, user_code, request_id, amount_sd, reward_amount_sd))
                
                # Obtener nombre del referidor
                cursor2.execute("SELECT fullname FROM users WHERE wallet_code = ?", (referred_by,))
                ref_user = cursor2.fetchone()
                referrer_fullname = ref_user[0] if ref_user else "Referidor"
                conn2.commit()
                conn2.close()
                
                # Enviar notificación al administrador (usuario '99999')
                add_notification(
                    "99999",
                    f"👥 <b>¡Comisión Pendiente de Referidos!</b> El usuario referido <b>{fullname}</b> ({user_code}) "
                    f"compró y fue aprobado por <b>{format_num(amount_sd)} SD</b>. "
                    f"Debes enviar una comisión del 20% (<b>{format_num(reward_amount_sd)} SD</b>) al referidor <b>{referrer_fullname}</b> (Billetera: <b>{referred_by}</b>)."
                )
        return success, msg
    conn.close()
    return False, "No se encontró la solicitud de compra."

def reject_purchase(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_code, amount_sd, amount_cop FROM purchase_requests WHERE id = ?", (request_id,))
    req = cursor.fetchone()
    if req:
        user_code, amount_sd, amount_cop = req
        cursor.execute("UPDATE purchase_requests SET status = 'REJECTED' WHERE id = ?", (request_id,))
        conn.commit()
        conn.close()
        
        # Enviar notificación oficial de rechazo
        add_notification(
            user_code, 
            f"🔴 <b>Compra rechazada.</b> El comprobante adjunto por <b>${amount_cop:,.0f} COP</b> fue rechazado "
            f"debido a inconsistencias. Verifica la imagen de Nequi e intenta nuevamente o ponte en contacto con soporte."
        )
        return True
    conn.close()
    return False


def toggle_user_vip_manually(wallet_code, enable):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fullname FROM users WHERE wallet_code = ?", (wallet_code,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return False, "No se encontró ningún usuario con ese código de billetera."
    
    fullname = user[0]
    is_vip_val = 1 if enable else 0
    cursor.execute("UPDATE users SET is_vip = ? WHERE wallet_code = ?", (is_vip_val, wallet_code))
    conn.commit()
    conn.close()
    
    if enable:
        add_notification(wallet_code, "👑 <b>¡Membresía VIP Activada!</b> El administrador te ha otorgado el rango VIP permanente. Ahora gozas de comisiones de retiro del 1% y bonos del 25% de por vida.")
        return True, f"✅ ¡Membresía VIP otorgada con éxito al usuario {fullname}!"
    else:
        add_notification(wallet_code, "⚠️ <b>Tu rango VIP ha sido desactivado</b> por el administrador. Tus comisiones de retiro han vuelto al 2% estándar.")
        return True, f"❌ ¡Membresía VIP removida con éxito al usuario {fullname}!"

def approve_purchase_as_vip(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.user_code, p.amount_sd, p.amount_cop, u.fullname, u.referred_by 
        FROM purchase_requests p 
        JOIN users u ON p.user_code = u.wallet_code 
        WHERE p.id = ?
    """, (request_id,))
    req = cursor.fetchone()
    if req:
        user_code, amount_sd, amount_cop, fullname, referred_by = req
        # Actualizar estado de la solicitud
        cursor.execute("UPDATE purchase_requests SET status = 'APPROVED' WHERE id = ?", (request_id,))
        # Activar VIP directamente
        cursor.execute("UPDATE users SET is_vip = 1 WHERE wallet_code = ?", (user_code,))
        conn.commit()
        conn.close()
        
        # Enviar los tokens desde la billetera maestra (99999) al comprador (que sirven como su reembolso o saldo comprado)
        success, msg = send_points("99999", user_code, amount_sd)
        if success:
            # Enviar notificación oficial de aprobación de VIP al comprador
            add_notification(
                user_code, 
                f"👑 <b>¡Membresía VIP Activada Directamente!</b> El administrador validó tu pago de <b>${amount_cop:,.0f} COP</b> y te ha activado el rango VIP permanente. "
                f"Se han acreditado <b>{format_num(amount_sd)} SD</b> a tu billetera y gozas de comisiones de retiro reducidas al 1% de por vida. ¡Disfruta tus privilegios!"
            )
            
            # Si tiene un referidor válido, calcular el 25% (ya que el usuario ahora es VIP) y crear registro de comisión pendiente
            if referred_by:
                conn2 = get_db_connection()
                cursor2 = conn2.cursor()
                cursor2.execute("SELECT is_vip FROM users WHERE wallet_code = ?", (referred_by,))
                ref_vip_row = cursor2.fetchone()
                is_ref_vip = ref_vip_row[0] if ref_vip_row else 0
                ref_pct = 0.25 if is_ref_vip == 1 else 0.20
                reward_amount_sd = amount_sd * ref_pct
                
                conn2 = get_db_connection()
                cursor2 = conn2.cursor()
                cursor2.execute("""
                    INSERT INTO referral_rewards (referrer_code, referred_code, purchase_id, purchase_amount_sd, reward_amount_sd, status)
                    VALUES (?, ?, ?, ?, ?, 'PENDING')
                """, (referred_by, user_code, request_id, amount_sd, reward_amount_sd))
                
                # Obtener nombre del referidor
                cursor2.execute("SELECT fullname FROM users WHERE wallet_code = ?", (referred_by,))
                ref_user = cursor2.fetchone()
                referrer_fullname = ref_user[0] if ref_user else "Referidor"
                conn2.commit()
                conn2.close()
                
                # Enviar notificación al administrador (usuario '99999')
                add_notification(
                    "99999",
                    f"👥 <b>¡Comisión de Referidos VIP!</b> El usuario referido <b>{fullname}</b> ({user_code}) "
                    f"activó VIP. "
                    f"Debes enviar una comisión de <b>{format_num(reward_amount_sd)} SD</b> al referidor <b>{referrer_fullname}</b> (Billetera: <b>{referred_by}</b>)."
                )
        return success, msg
    conn.close()
    return False, "No se encontró la solicitud de compra."

# --- LLAMADOS A API Y CACHÉ ---

@st.cache_data(ttl=120)
def fetch_btc_price():
    try:
        response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return float(data['data']['amount'])
    except Exception:
        pass
    return 64320.50

@st.cache_data(ttl=10) # Cache for 10 seconds to keep it super fresh
def fetch_sd_price_from_dexscreener():
    # 1. Intentar con DexScreener
    try:
        url = "https://api.dexscreener.com/latest/dex/tokens/0xC324649213ec1757190bc4b78bcD41Cc1545C264"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data and 'pairs' in data and data['pairs'] is not None and len(data['pairs']) > 0:
                pair = data['pairs'][0]
                price_usd = float(pair.get('priceUsd', 0.0))
                if price_usd > 0:
                    return price_usd
    except Exception:
        pass

    # 2. Intentar con GeckoTerminal (Excelente respaldo para pools de BNB que DexScreener no indexa rápido en su API de tokens)
    try:
        url = "https://api.geckoterminal.com/api/v2/networks/bsc/tokens/0xC324649213ec1757190bc4b78bcD41Cc1545C264"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data and 'data' in data and 'attributes' in data['data']:
                price_usd = float(data['data']['attributes'].get('price_usd', 0.0))
                if price_usd > 0:
                    return price_usd
    except Exception:
        pass
    return None

@st.cache_data(ttl=120)
def fetch_usd_cop_rate():
    try:
        response = requests.get("https://economia.awesomeapi.com.br/json/last/USD-COP", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return float(data['USDCOP']['bid'])
    except Exception:
        pass
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return float(data['rates']['COP'])
    except Exception:
        pass
    return 4150.00 # Real-world close average fallback


@st.cache_data(ttl=600)
def get_btc_historical_data():
    try:
        response = requests.get("https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=30", timeout=2)
        if response.status_code == 200:
            data = response.json()
            prices = data['Data']['Data']
            df = pd.DataFrame(prices)
            df['Fecha'] = pd.to_datetime(df['time'], unit='s')
            df['Precio (USD)'] = df['close']
            return df[['Fecha', 'Precio (USD)']]
    except Exception:
        pass
    dates = pd.date_range(end=datetime.now(), periods=30)
    np.random.seed(42)
    base = 61200
    prices = [base + i*160 + np.random.normal(0, 700) for i in range(30)]
    return pd.DataFrame({"Fecha": dates, "Precio (USD)": prices})

@st.cache_data(ttl=600)
def get_usd_cop_historical_data():
    try:
        response = requests.get("https://economia.awesomeapi.com.br/json/daily/USD-COP/30", timeout=2)
        if response.status_code == 200:
            data = response.json()
            rates = []
            dates = []
            for item in data:
                rates.append(float(item['bid']))
                timestamp = int(item['timestamp'])
                dates.append(pd.to_datetime(timestamp, unit='s'))
            df = pd.DataFrame({"Fecha": dates, "Tasa (COP)": rates})
            df = df.sort_values(by="Fecha").reset_index(drop=True)
            return df
    except Exception:
        pass
    dates = pd.date_range(end=datetime.now(), periods=30)
    np.random.seed(10)
    rates = [4150 - i*5 + np.random.normal(0, 25) for i in range(30)]
    return pd.DataFrame({"Fecha": dates, "Tasa (COP)": rates})

def get_custom_token_historical_data(current_price):
    dates = pd.date_range(end=datetime.now(), periods=30)
    np.random.seed(100)
    prices = []
    base = current_price * 0.75
    for i in range(29):
        pct_change = np.random.normal(0.008, 0.04)
        base = base * (1 + pct_change)
        prices.append(base)
    prices.append(current_price)
    return pd.DataFrame({"Fecha": dates, "Precio (USD)": prices})

# --- LÓGICA DE NEGOCIO ---

def register_user(username, password, fullname, email, referred_by=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    wallet_code = generate_unique_wallet_code()
    
    if referred_by:
        referred_by = referred_by.strip()
        if len(referred_by) != 5 or not referred_by.isdigit():
            conn.close()
            return False, "El código de referido debe ser de exactamente 5 dígitos numéricos."
        cursor.execute("SELECT fullname FROM users WHERE wallet_code = ?", (referred_by,))
        if not cursor.fetchone():
            conn.close()
            return False, f"El código de referido {referred_by} no corresponde a ningún usuario registrado."
            
    try:
        cursor.execute("""
            INSERT INTO users (username, password, fullname, email, wallet_code, balance, is_admin, referred_by)
            VALUES (?, ?, ?, ?, ?, 0.0, 0, ?)
        """, (username, hashed_pw, fullname, email, wallet_code, referred_by))
        conn.commit()
        conn.close()
        
        # Enviar notificación inicial de bienvenida
        add_notification(
            wallet_code, 
            f"🎉 <b>¡Te damos la bienvenida a Alianza CryptoWallet!</b> Tu cuenta ha sido creada con éxito. "
            f"Tu código de billetera inmutable es <b>{wallet_code}</b>. Explora tus balances e historial."
        )
        
        # Enviar notificación al referidor
        if referred_by:
            add_notification(
                referred_by,
                f"👥 <b>¡Nuevo Referido Registrado!</b> El usuario <b>{fullname}</b> se ha registrado usando tu código de invitación. "
                f"Recibirás una bonificación del 20% en tokens SD de cada compra verificada que realice."
            )
            
        return True, wallet_code
    except sqlite3.IntegrityError:
        conn.close()
        return False, "El nombre de usuario ya está registrado."

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    cursor.execute("""
        SELECT id, username, fullname, email, wallet_code, balance, is_admin 
        FROM users WHERE username = ? AND password = ?
    """, (username, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    return user

def change_user_password(username, old_password, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_old = hash_password(old_password)
    cursor.execute("SELECT 1 FROM users WHERE username = ? AND password = ?", (username, hashed_old))
    if not cursor.fetchone():
        conn.close()
        return False, "La contraseña actual es incorrecta."
    
    hashed_new = hash_password(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new, username))
    conn.commit()
    conn.close()
    return True, "Contraseña cambiada exitosamente."

def send_points(sender_code, receiver_code, amount):
    if sender_code == receiver_code:
        return False, "No puedes enviarte puntos a ti mismo."
    if amount <= 0:
        return False, "El monto debe ser mayor a cero."
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar remitente (si no es el sistema/admin)
    if sender_code != "99999":
        cursor.execute("SELECT balance FROM users WHERE wallet_code = ?", (sender_code,))
        sender = cursor.fetchone()
        if not sender or sender[0] < amount:
            conn.close()
            return False, "Saldo de tokens insuficiente."
            
    # Verificar destinatario
    cursor.execute("SELECT username, fullname FROM users WHERE wallet_code = ?", (receiver_code,))
    receiver = cursor.fetchone()
    if not receiver:
        conn.close()
        return False, f"El código de billetera {receiver_code} no existe."
    
    receiver_name = receiver[1]
        
    try:
        if sender_code != "99999":
            cursor.execute("UPDATE users SET balance = balance - ?, wallet_code = wallet_code WHERE wallet_code = ?", (amount, sender_code))
        else:
            cursor.execute("UPDATE users SET balance = balance - ?, wallet_code = wallet_code WHERE wallet_code = ?", (amount, sender_code))
            
        cursor.execute("UPDATE users SET balance = balance + ?, wallet_code = wallet_code WHERE wallet_code = ?", (amount, receiver_code))
        
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES (?, ?, ?)
        """, (sender_code, receiver_code, amount))
        
        conn.commit()
        conn.close()
        
        # Enviar notificación al receptor si la transacción no es automática del admin
        if sender_code != "99999":
            add_notification(
                receiver_code,
                f"📥 <b>¡Has recibido fondos!</b> El código de billetera <b>{sender_code}</b> te ha enviado "
                f"<b>{format_num(amount)} SD</b> de forma directa."
            )
        
        return True, f"¡Acreditación exitosa! Has enviado {format_num(amount)} tokens."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error en la transacción: {str(e)}"

def get_user_balance(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance, wallet_code, balance_cop, is_vip FROM users WHERE username = ?", (username,))
    res = cursor.fetchone()
    conn.close()
    return res if res else (0.0, "", 0.0, 0)


def format_num(val):
    if val is None:
        return "0"
    try:
        val_f = float(val)
        if val_f.is_integer() or abs(val_f - round(val_f)) < 1e-9:
            return f"{int(round(val_f)):,}"
        formatted = f"{val_f:,.2f}"
        if '.' in formatted:
            formatted = formatted.rstrip('0').rstrip('.')
        return formatted
    except Exception:
        return str(val)

def update_user_balance_and_cop(user_code, balance_sd, balance_cop):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users 
        SET balance = ?, balance_cop = ? 
        WHERE wallet_code = ?
    """, (balance_sd, balance_cop, user_code))
    conn.commit()
    conn.close()


def get_user_nequi(wallet_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nequi_number FROM users WHERE wallet_code = ?", (wallet_code,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res and res[0] else ""

def update_user_nequi(wallet_code, nequi_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET nequi_number = ? WHERE wallet_code = ?", (nequi_number, wallet_code))
    conn.commit()
    conn.close()
    return True

def update_global_nequi(nequi_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Actualizar la cuenta madre global en token_settings
    cursor.execute("UPDATE token_settings SET nequi_number = ? WHERE id = 1", (nequi_number,))
    # Sincronizar el nequi_number del propio admin en la tabla de usuarios
    cursor.execute("UPDATE users SET nequi_number = ? WHERE wallet_code = '99999'", (nequi_number,))
    conn.commit()
    conn.close()
    return True

# --- LÓGICA DE MENSAJERÍA Y MÓVILES (EMPRESA DE MENSAJERÍA) ---

def pay_delivery_service(sender_code, driver_code, amount_sd, service_id=""):
    if sender_code == driver_code:
        return False, "No puedes pagarte un envío a ti mismo."
    if amount_sd <= 0:
        return False, "El monto del envío debe ser mayor a cero."
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Verificar saldo en SD del cliente
    cursor.execute("SELECT balance, fullname FROM users WHERE wallet_code = ?", (sender_code,))
    sender = cursor.fetchone()
    if not sender or sender[0] < amount_sd:
        conn.close()
        return False, "Saldo de tokens SIAD (SD) insuficiente para pagar este envío."
    sender_name = sender[1]
    
    # 2. Verificar existencia del conductor (móvil)
    cursor.execute("SELECT fullname FROM users WHERE wallet_code = ?", (driver_code,))
    driver = cursor.fetchone()
    if not driver:
        conn.close()
        return False, f"El código de billetera del móvil {driver_code} no existe o no es válido."
    driver_name = driver[0]
    
    # 3. Calcular montos de subsidio automático
    cashback_sd = amount_sd * 0.50
    bonus_sd = amount_sd * 0.10
    total_admin_subsidy = cashback_sd + bonus_sd
    
    # Verificar si el administrador (billetera maestra 99999) tiene fondos suficientes
    cursor.execute("SELECT balance FROM users WHERE wallet_code = '99999'")
    admin_bal = cursor.fetchone()
    if not admin_bal or admin_bal[0] < total_admin_subsidy:
        conn.close()
        return False, "La billetera del administrador no dispone de fondos de base suficientes para financiar el subsidio en este momento."
        
    try:
        # 4. Descontar del cliente y sumarle al conductor (Pago original)
        cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (amount_sd, sender_code))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (amount_sd, driver_code))
        
        # Registrar transacción original
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES (?, ?, ?)
        """, (sender_code, driver_code, amount_sd))
        
        # 5. Enviar reembolso del 50% al cliente desde el Admin (99999)
        cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (cashback_sd,))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (cashback_sd, sender_code))
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES ('99999', ?, ?)
        """, (sender_code, cashback_sd))
        
        # 6. Enviar bono del 10% al móvil desde el Admin (99999)
        cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (bonus_sd,))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (bonus_sd, driver_code))
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES ('99999', ?, ?)
        """, (driver_code, bonus_sd))
        
        # 7. Registrar en la tabla de pagos de móviles (Mensajería)
        token_price_usd = get_token_settings()['price_usd']
        usd_cop_rate = fetch_usd_cop_rate()
        amount_cop = amount_sd * token_price_usd * usd_cop_rate
        
        cursor.execute("""
            INSERT INTO movil_payments (user_code, payment_type, amount_sd, amount_cop, target_code)
            VALUES (?, 'SHIPPING_PAYMENT', ?, ?, ?)
        """, (sender_code, amount_sd, amount_cop, driver_code))
        
        conn.commit()
        conn.close()
        
        # 8. Notificaciones
        lbl_service = f" (ID Guía: {service_id})" if service_id else ""
        add_notification(
            sender_code,
            f"📦 <b>¡Pago de Envío Realizado!</b> Pagaste <b>{format_num(amount_sd)} SD</b> "
            f"(${amount_cop:,.0f} COP) al móvil <b>{driver_name} ({driver_code})</b>{lbl_service}. "
            f"🔥 <b>¡Subsidio Alianza!</b> Se te ha devuelto un reembolso del 50% (<b>{format_num(cashback_sd)} SD</b>) a tu billetera de forma automática. <b>¡El envío te costó la mitad!</b>"
        )
        add_notification(
            driver_code,
            f"📦 <b>¡Pago de Envío Recibido!</b> El cliente <b>{sender_name}</b> te pagó <b>{format_num(amount_sd)} SD</b> "
            f"(${amount_cop:,.0f} COP){lbl_service}. "
            f"🚀 <b>¡Bono Alianza!</b> Recibiste un bono del 10% adicional (<b>{format_num(bonus_sd)} SD</b>) del fondo del Administrador. "
            f"Total recibido: <b>{(amount_sd + bonus_sd):,.4f} SD</b>."
        )
        return True, f"¡Pago exitoso! Enviaste {format_num(amount_sd)} SD, se te reembolsó el 50% de inmediato ({format_num(cashback_sd)} SD) y el conductor recibió {amount_sd + bonus_sd:,.4f} SD (10% bono)."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar el pago del envío: {str(e)}"

def pay_weekly_fee(user_code, use_tokens=True, message=""): 
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obtener datos del usuario
    cursor.execute("SELECT balance, balance_cop, fullname FROM users WHERE wallet_code = ?", (user_code,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return False, "Usuario no encontrado."
    
    balance_sd, balance_cop, fullname = user
    token = get_token_settings()
    usd_cop_rate = fetch_usd_cop_rate()
    token_price_cop = token['price_usd'] * usd_cop_rate
    
    try:
        if use_tokens:
            # Cuota de 40.000 COP con 20% descuento = 32.000 COP
            fee_cop = 32000.0
            fee_sd = fee_cop / token_price_cop
            
            if balance_sd < fee_sd:
                conn.close()
                return False, f"Saldo en SD insuficiente. Necesitas {format_num(fee_sd)} SD para pagar con descuento del 20%."
                
            # Cobrar en SD (enviar a la cuenta del admin '99999')
            cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (fee_sd, user_code))
            cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (fee_sd, '99999'))
            
            # Registrar en transactions
            cursor.execute("""
                INSERT INTO transactions (sender_code, receiver_code, amount)
                VALUES (?, '99999', ?)
            """, (user_code, fee_sd))
            
            # Registrar en movil_payments
            cursor.execute("""
                INSERT INTO movil_payments (user_code, payment_type, amount_sd, amount_cop, target_code, message)
                VALUES (?, 'WEEKLY_FEE_SD', ?, ?, '99999', ?)
            """, (user_code, fee_sd, fee_cop, message or ''))
            
            conn.commit()
            conn.close()
            
            # Notificaciones
            add_notification(
                user_code,
                f"💳 <b>¡Cuota Semanal Pagada!</b> Has pagado tu cuota de móvil por valor de <b>$32,000 COP</b> "
                f"(pagados con <b>{format_num(fee_sd)} SD</b> tras aplicar un 20% de descuento). ¡Gracias por tu pago!"
            )
            add_notification(
                '99999',
                f"🚚 <b>¡Pago de Cuota Recibido!</b> El móvil <b>{fullname} ({user_code})</b> ha pagado su cuota semanal "
                f"usando tokens SD (Recibido: <b>{format_num(fee_sd)} SD</b> equivalente a $32,000 COP)." + (f"<br>💬 <b>Mensaje:</b> {message}" if message else "")
            )
            return True, f"Cuota de móvil pagada con éxito usando {format_num(fee_sd)} SD ($32,000 COP)."
            
        else:
            # Cuota sin descuento = 40.000 COP
            fee_cop = 40000.0
            
            if balance_cop < fee_cop:
                conn.close()
                return False, "Saldo de pesos colombianos (COP) retirable insuficiente para pagar la cuota de $40,000 COP."
                
            # Cobrar en COP del saldo del usuario y sumarlo al del admin
            cursor.execute("UPDATE users SET balance_cop = balance_cop - ? WHERE wallet_code = ?", (fee_cop, user_code))
            cursor.execute("UPDATE users SET balance_cop = balance_cop + ? WHERE wallet_code = ?", (fee_cop, '99999'))
            
            # Registrar en transactions (equivalente en SD para registro histórico)
            cursor.execute("""
                INSERT INTO transactions (sender_code, receiver_code, amount)
                VALUES (?, '99999_COP', ?)
            """, (user_code, fee_cop / token_price_cop))
            
            # Registrar en movil_payments
            cursor.execute("""
                INSERT INTO movil_payments (user_code, payment_type, amount_sd, amount_cop, target_code, message)
                VALUES (?, 'WEEKLY_FEE_COP', ?, ?, '99999', ?)
            """, (user_code, fee_cop / token_price_cop, fee_cop, message or ''))
            
            conn.commit()
            conn.close()
            
            # Notificaciones
            add_notification(
                user_code,
                f"💳 <b>¡Cuota Semanal Pagada!</b> Has pagado tu cuota de móvil de <b>$40,000 COP</b> "
                f"(debitados de tu saldo retirable en pesos). ¡Gracias por tu pago!"
            )
            add_notification(
                '99999',
                f"🚚 <b>¡Pago de Cuota Recibido!</b> El móvil <b>{fullname} ({user_code})</b> ha pagado su cuota semanal "
                f"en pesos colombianos ($40,000 COP)." + (f"<br>💬 <b>Mensaje:</b> {message}" if message else "")
            )
            return True, "Cuota de móvil pagada con éxito usando $40,000 COP de tu saldo retirable."
            
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar el pago de la cuota: {str(e)}"

def get_movil_payments_history(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.payment_type, p.amount_sd, p.amount_cop, p.target_code, p.timestamp, p.message, 
               u1.fullname as customer_name, u2.fullname as driver_name
        FROM movil_payments p
        LEFT JOIN users u1 ON p.user_code = u1.wallet_code
        LEFT JOIN users u2 ON p.target_code = u2.wallet_code
        WHERE p.user_code = ? OR p.target_code = ?
        ORDER BY p.timestamp DESC
    """, conn, params=(user_code, user_code))
    conn.close()
    return df

def get_all_movil_payments():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.payment_type, p.amount_sd, p.amount_cop, p.user_code, p.target_code, p.timestamp, p.message, 
               u1.fullname as customer_name, u2.fullname as target_name
        FROM movil_payments p
        LEFT JOIN users u1 ON p.user_code = u1.wallet_code
        LEFT JOIN users u2 ON p.target_code = u2.wallet_code
        ORDER BY p.timestamp DESC
    """, conn)
    conn.close()
    return df


def get_transaction_history(wallet_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT t.id, t.sender_code, t.receiver_code, t.amount, t.timestamp,
               u1.fullname as sender_name, u2.fullname as receiver_name
        FROM transactions t
        LEFT JOIN users u1 ON t.sender_code = u1.wallet_code
        LEFT JOIN users u2 ON t.receiver_code = u2.wallet_code
        WHERE t.sender_code = ? OR t.receiver_code = ?
        ORDER BY t.timestamp ASC
    """, conn, params=(wallet_code, wallet_code))
    conn.close()
    return df

def swap_sd_to_cop(user_code, amount_sd, rate_usd, usd_cop_rate):
    if amount_sd <= 0:
        return False, "La cantidad de SD debe ser mayor a cero."
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE wallet_code = ?", (user_code,))
    res = cursor.fetchone()
    if not res or res[0] < amount_sd:
        conn.close()
        return False, "Saldo de tokens SD insuficiente."
    
    # Calcular valor en pesos COP
    usd_value = amount_sd * rate_usd
    cop_value = usd_value * usd_cop_rate
    
    try:
        # Descontar SD, aumentar balance_cop
        cursor.execute("UPDATE users SET balance = balance - ?, balance_cop = balance_cop + ? WHERE wallet_code = ?", (amount_sd, cop_value, user_code))
        
        # Registrar como transacción de swap
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES (?, 'SWAP_COP', ?)
        """, (user_code, amount_sd))
        
        conn.commit()
        conn.close()
        
        # Enviar notificación
        add_notification(
            user_code,
            f"🔄 <b>Swap completado exitosamente:</b> Has cambiado <b>{format_num(amount_sd)} SD</b> por un valor de <b>${cop_value:,.0f} COP</b>. El saldo se ha acreditado a tu cuenta."
        )
        return True, f"¡Swap exitoso! Has convertido {format_num(amount_sd)} SD a ${cop_value:,.0f} COP."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar el swap: {str(e)}"

def submit_withdrawal_request(user_code, amount_cop, nequi_number):
    if amount_cop < 1000:
        return False, "El monto mínimo de retiro es de $1,000 pesos colombianos (COP)."
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance_cop, is_vip FROM users WHERE wallet_code = ?", (user_code,))
    res = cursor.fetchone()
    if not res or res[0] < amount_cop:
        conn.close()
        return False, "Saldo en pesos (COP) insuficiente para procesar el retiro."
    
    is_vip = res[1] if len(res) > 1 else 0
    fee_pct = 0.01 if is_vip == 1 else 0.02
    fee_cop = amount_cop * fee_pct
    net_cop = amount_cop - fee_cop
    
    try:
        # Descontar saldo de pesos COP de forma inmediata (congelar saldo para retiro)
        cursor.execute("UPDATE users SET balance_cop = balance_cop - ? WHERE wallet_code = ?", (amount_cop, user_code))
        
        # Registrar solicitud de retiro pendiente
        cursor.execute("""
            INSERT INTO withdrawal_requests (user_code, amount_cop, fee_cop, net_cop, nequi_number, status)
            VALUES (?, ?, ?, ?, ?, 'PENDING')
        """, (user_code, amount_cop, fee_cop, net_cop, nequi_number))
        
        conn.commit()
        conn.close()
        
        # Notificar al usuario
        add_notification(
            user_code,
            f"💸 <b>Solicitud de retiro recibida:</b> Has solicitado un retiro por <b>${amount_cop:,.0f} COP</b> a tu cuenta Nequi <b>{nequi_number}</b>. "
            f"Comisión del 2% (${fee_cop:,.0f} COP) deducida. Recibirás neto <b>${net_cop:,.0f} COP</b> una vez que el administrador lo apruebe."
        )
        return True, "Solicitud de retiro enviada con éxito. El administrador la validará pronto."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar el retiro: {str(e)}"

def get_pending_withdrawals():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT w.id, w.user_code, w.amount_cop, w.fee_cop, w.net_cop, w.nequi_number, w.timestamp, u.fullname, u.username
        FROM withdrawal_requests w
        JOIN users u ON w.user_code = u.wallet_code
        WHERE w.status = 'PENDING'
        ORDER BY w.timestamp ASC
    """, conn)
    conn.close()
    return df

def get_user_withdrawals(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT id, amount_cop, fee_cop, net_cop, nequi_number, receipt_image, status, timestamp
        FROM withdrawal_requests
        WHERE user_code = ?
        ORDER BY timestamp DESC
    """, conn, params=(user_code,))
    conn.close()
    return df
def get_platform_fees_summary():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Total fees generated
    cursor.execute("SELECT SUM(fee_cop) FROM withdrawal_requests WHERE status = 'APPROVED'")
    total_fees = cursor.fetchone()[0] or 0.0
    
    # Locked fees (approved within the last 24 hours)
    # Compare against UTC since SQLite uses UTC CURRENT_TIMESTAMP
    cursor.execute("""
        SELECT SUM(fee_cop) FROM withdrawal_requests 
        WHERE status = 'APPROVED' AND approved_at >= datetime('now', '-1 day')
    """)
    locked_fees = cursor.fetchone()[0] or 0.0
    
    # Available fees (approved more than 24 hours ago)
    cursor.execute("""
        SELECT SUM(fee_cop) FROM withdrawal_requests 
        WHERE status = 'APPROVED' AND fee_status = 'UNCLAIMED' AND (approved_at < datetime('now', '-1 day') OR approved_at IS NULL)
    """)
    available_fees = cursor.fetchone()[0] or 0.0
    
    conn.close()
    return total_fees, locked_fees, available_fees

def claim_platform_fees():
    total_fees, locked_fees, available_fees = get_platform_fees_summary()
    if available_fees <= 0:
        return False, "No hay comisiones de plataforma liberadas disponibles para reclamar en este momento."
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Mark as CLAIMED
        cursor.execute("""
            UPDATE withdrawal_requests 
            SET fee_status = 'CLAIMED' 
            WHERE status = 'APPROVED' AND fee_status = 'UNCLAIMED' AND (approved_at < datetime('now', '-1 day') OR approved_at IS NULL)
        """)
        # Add to admin's balance_cop
        cursor.execute("UPDATE users SET balance_cop = balance_cop + ? WHERE username = 'admin'", (available_fees,))
        conn.commit()
        conn.close()
        return True, f"¡Éxito! Se han transferido ${available_fees:,.0f} COP de comisiones liberadas a tu balance en pesos de administrador."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al reclamar comisiones: {str(e)}"

def get_approved_withdrawals_fees():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT w.id, w.user_code, w.amount_cop, w.fee_cop, w.approved_at, w.fee_status, u.fullname
        FROM withdrawal_requests w
        JOIN users u ON w.user_code = u.wallet_code
        WHERE w.status = 'APPROVED'
        ORDER BY w.approved_at DESC
    """, conn)
    conn.close()
    return df


def approve_withdrawal(request_id, receipt_bytes):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_code, amount_cop, fee_cop, net_cop, nequi_number FROM withdrawal_requests WHERE id = ?", (request_id,))
    res = cursor.fetchone()
    if res:
        user_code, amount_cop, fee_cop, net_cop, nequi_number = res
        try:
            cursor.execute("UPDATE withdrawal_requests SET status = 'APPROVED', receipt_image = ?, approved_at = CURRENT_TIMESTAMP WHERE id = ?", (receipt_bytes, request_id))
            conn.commit()
            conn.close()
            
            # Enviar notificación oficial con el comprobante adjunto
            add_notification(
                user_code,
                f"🟢 <b>¡Retiro aprobado y pagado!</b> El administrador confirmó el envío de <b>${net_cop:,.0f} COP</b> "
                f"a tu cuenta Nequi <b>{nequi_number}</b> (descontando la comisión del 2% de ${fee_cop:,.0f} COP). "
                f"La captura del comprobante oficial ha sido adjuntada con éxito en tu historial."
            )
            return True, "Retiro aprobado con éxito. El comprobante ha sido compartido con el usuario."
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, f"Error al aprobar retiro: {str(e)}"
    conn.close()
    return False, "No se encontró la solicitud de retiro."

def reject_withdrawal(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_code, amount_cop FROM withdrawal_requests WHERE id = ?", (request_id,))
    res = cursor.fetchone()
    if res:
        user_code, amount_cop = res
        try:
            cursor.execute("UPDATE withdrawal_requests SET status = 'REJECTED' WHERE id = ?", (request_id,))
            # Devolver saldo de COP al usuario
            cursor.execute("UPDATE users SET balance_cop = balance_cop + ? WHERE wallet_code = ?", (amount_cop, user_code))
            conn.commit()
            conn.close()
            
            # Notificar al usuario
            add_notification(
                user_code,
                f"🔴 <b>Retiro rechazado:</b> Tu solicitud de retiro por <b>${amount_cop:,.0f} COP</b> fue rechazada. "
                f"Los fondos congelados han sido reembolsados en su totalidad a tu saldo retirable (COP)."
            )
            return True
        except Exception as e:
            conn.rollback()
            conn.close()
            return False
    conn.close()
    return False

# --- INTERFAZ GRÁFICA ---

# Estilo visual moderno premium: Negro Absoluto, Amarillo Dorado y Botones Verdes con Borde Dorado
st.markdown("""
    <style>
    /* Ocultar marca de Streamlit para que parezca una App propia */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    
    /* Mantener visible la cabecera para el botón de despliegue del menú pero totalmente transparente */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        background: transparent !important;
    }
    /* Fondo principal Negro Puro */
    .main {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    /* Botones Verdes Cripto con Bordes Dorados */
    .stButton>button {
        background: #10b981 !important; /* Verde cripto */
        color: #000000 !important; /* Texto negro para alto contraste */
        border: 2px solid #ffd700 !important; /* Borde dorado */
        border-radius: 6px !important;
        font-weight: 800 !important;
        padding: 0.4rem 1.0rem !important;
        font-size: 0.85rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    .stButton>button:hover {
        background: #059669 !important; /* Verde cripto oscuro al hover */
        border-color: #ffffff !important; /* Borde brilla blanco/dorado */
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4) !important; /* Glow verde cripto */
    }
    
    /* Tarjetas Negras/Grises con Bordes Dorados */
    .card {
        background-color: #0d0d11 !important;
        padding: 1.0rem !important;
        border-radius: 10px !important;
        border: 1px solid #ffd700 !important; /* Delicado borde dorado */
        margin-bottom: 0.8rem !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.03) !important;
    }
    
    /* Notificaciones estilizadas */
    .notification-card {
        background-color: #0d0d11 !important;
        padding: 1rem !important;
        border-radius: 6px !important;
        border-left: 4px solid #ffd700 !important;
        border-right: 1px solid #1a1a24 !important;
        border-top: 1px solid #1a1a24 !important;
        border-bottom: 1px solid #1a1a24 !important;
        margin-bottom: 0.8rem !important;
    }
    
    /* Textos en Amarillo Dorado */
    .golden-title {
        color: #ffd700 !important;
        font-weight: 700 !important;
    }
    
    .metric-title {
        color: #ffd700 !important; /* Amarillo dorado */
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.07em;
    }
    .metric-value {
        font-size: 1.55rem;
        font-weight: 800;
        margin: 5px 0;
        color: #ffffff;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #a1a1aa;
    }
    
    /* Estilización del menú lateral */
    section[data-testid="stSidebar"] {
        background-color: #060608 !important;
        border-right: 2px solid #ffd700 !important; /* Línea divisoria dorada */
    }
    
    /* Evitar la línea amarilla huérfana en el borde de la pantalla cuando el menú se minimiza por completo */
    section[data-testid="stSidebar"][data-collapsed="true"] {
        border-right: none !important;
    }
    
    /* Input fields estilizados */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #0d0d11 !important;
        color: #ffffff !important;
        border: 1px solid #3f3f46 !important;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #ffd700 !important;
    }

    /* Ocultar por completo el círculo de selección de radio nativo de Streamlit */
    div[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label > div:first-child {
        display: none !important;
    }

    /* CONVERTIR MENÚ EN BOTONES/CUADROS GRANDES DE NAVEGACIÓN (TIPO CERRAR SESIÓN PERO AZUL/DORADO Y EFECTO BLOB) */
    div[data-testid="stSidebar"] div[data-testid="stRadio"] > label {
        color: #ffd700 !important; /* Título en Amarillo Dorado */
        font-size: 1.15rem !important;
        font-weight: 850 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 15px !important;
        display: block !important;
        text-align: center !important;
        border-bottom: 2px solid #ffd70033 !important;
        padding-bottom: 8px !important;
    }

    div[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label {
        padding: 14px 12px !important; /* Más grandes, amplios y cómodos */
        min-height: 56px !important; /* Altura ideal de botón táctil premium */
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important; /* Fondo tipo botón azul oscuro/slate */
        border: 2px solid #ffd70088 !important; /* Borde dorado sólido como el botón de Cerrar Sesión */
        border-radius: 8px !important; /* Bordes redondeados de botón */
        width: 100% !important; /* Cubre todo el ancho del sidebar */
        display: flex !important;
        justify-content: center !important; /* Centrado absoluto del texto */
        align-items: center !important;
        cursor: pointer !important;
        margin: 0 !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4) !important; /* Sombra tridimensional */
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    /* Separación entre botones independientes */
    div[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] > div {
        margin-bottom: 14px !important; /* Separación amplia para diseño limpio */
    }

    /* Efecto Hover: Brillo, elevación y borde blanco */
    div[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label:hover {
        border-color: #ffffff !important; /* El borde brilla en blanco */
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%) !important; /* Azul más vivo */
        box-shadow: 0 6px 18px rgba(30, 64, 175, 0.5) !important; /* Glow azul */
        transform: translateY(-2px) !important; /* Elevación física */
    }

    /* EFECTO CLICK ELÁSTICO (BLOB / BURBUJA LÍQUIDA AL PRESIONAR) */
    div[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label:active {
        transform: scale(0.91) translateY(2px) !important; /* Se encoge y baja en el click */
        border-radius: 18px !important; /* Se deforma como una burbuja/blob líquido */
        border-color: #ffffff !important; /* El borde destella blanco */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.6) !important;
        transition: transform 0.05s ease-out, border-radius 0.05s ease-out !important;
    }

    /* Texto súper claro, grande y legible dentro de cada botón */
    div[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label [data-testid="stMarkdownContainer"] p {
        font-size: 1.12rem !important; /* Letra más grande y legible */
        font-weight: 850 !important; /* Extra grueso de alta visibilidad */
        color: #ffffff !important; /* Color blanco de base */
        text-align: center !important;
        width: 100% !important;
        letter-spacing: 0.03em !important;
        margin: 0 !important;
        text-transform: capitalize !important;
    }

    /* CUANDO EL BOTÓN ESTÁ SELECCIONADO (ESTADO ACTIVO DE LA VENTANA) */
    div[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label:has(input[type="radio"]:checked) {
        border-color: #ffd700 !important; /* Borde dorado brillante */
        border-width: 2.5px !important;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important; /* Degradado azul zafiro premium */
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important; /* Brillo azul */
    }

    /* Color de texto dorado cuando el botón está seleccionado/activo */
    div[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label:has(input[type="radio"]:checked) [data-testid="stMarkdownContainer"] p {
        color: #ffd700 !important; /* Texto en amarillo dorado para resaltar la ventana activa */
    }

    </style>
""", unsafe_allow_html=True)

# Inicializar sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.fullname = None
    st.session_state.email = None
    st.session_state.wallet_code = None
    st.session_state.is_admin = False


# Cargar configuraciones del token personalizado (Alianza - SD)
token = get_token_settings()

# Cargar cotizaciones globales via API
btc_price = fetch_btc_price()
usd_cop = fetch_usd_cop_rate()

# Cargar precio en tiempo real de DexScreener (Contrato: 0xC324649213ec1757190bc4b78bcD41Cc1545C264)
live_sd_price = fetch_sd_price_from_dexscreener()
if live_sd_price is not None and live_sd_price > 0:
    token_price_usd = live_sd_price
    # Sincronizar automáticamente en la BD para que quede actualizado si el admin no lo cambia manualmente
    try:
        conn_sync = get_db_connection()
        cursor_sync = conn_sync.cursor()
        cursor_sync.execute("UPDATE token_settings SET token_price_usd = ? WHERE id = 1", (live_sd_price,))
        conn_sync.commit()
        conn_sync.close()
    except Exception:
        pass
else:
    token_price_usd = token['price_usd']

token_price_cop = token_price_usd * usd_cop

# El administrador ahora controla los precios de la membresía en la tienda directamente desde el panel de control.
# Ya no se fuerza automáticamente de forma dinámica al arrancar, respetando el valor guardado en base de datos.


if not st.session_state.logged_in:
    st.sidebar.title("🔐 Alianza CryptoWallet")
    menu = st.sidebar.selectbox("Seleccione una opción", ["Iniciar Sesión", "Registrarse"])
    
    if menu == "Iniciar Sesión":
        st.markdown("<h2 class='golden-title'>🔑 Iniciar Sesión</h2>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Nombre de Usuario", placeholder="Ej. juan123")
            password = st.text_input("Contraseña", type="password", placeholder="******")
            submit = st.form_submit_button("Ingresar")
            
            if submit:
                if username and password:
                    user = login_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user[0]
                        st.session_state.username = user[1]
                        st.session_state.fullname = user[2]
                        st.session_state.email = user[3]
                        st.session_state.wallet_code = user[4]
                        st.session_state.is_admin = bool(user[6])
                        st.success(f"¡Bienvenido de nuevo, {user[2]}!")
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos.")
                else:
                    st.warning("Por favor completa todos los campos.")
                    
    elif menu == "Registrarse":
        st.markdown("<h2 class='golden-title'>📝 Registro de Cuenta</h2>", unsafe_allow_html=True)
        with st.form("register_form"):
            fullname = st.text_input("Nombre Completo", placeholder="Ej. Juan Pérez")
            email = st.text_input("Correo Electrónico", placeholder="Ej. juan@correo.com")
            username = st.text_input("Nombre de Usuario Único", placeholder="Ej. juan123")
            password = st.text_input("Contraseña", type="password", placeholder="Mínimo 6 caracteres")
            confirm_password = st.text_input("Confirmar Contraseña", type="password", placeholder="******")
            referred_by = st.text_input("Código de Referido (Opcional - 5 dígitos)", max_chars=5, placeholder="Ej. 12345")
            submit = st.form_submit_button("Crear Cuenta")
            
            if submit:
                if not (fullname and email and username and password and confirm_password):
                    st.warning("Todos los campos son obligatorios.")
                elif password != confirm_password:
                    st.error("Las contraseñas no coinciden.")
                elif len(password) < 6:
                    st.error("La contraseña debe tener al menos 6 caracteres.")
                else:
                    ref_code = referred_by.strip() if referred_by else None
                    success, result = register_user(username, password, fullname, email, ref_code)
                    if success:
                        st.balloons()
                        st.success("¡Registro Exitoso!")
                        st.markdown(f"""
                        <div class="card" style="border-left: 5px solid #ffd700;">
                            <h4 style='color: #ffd700; margin:0;'>🔐 Tu Código de Billetera Único (Inmutable)</h4>
                            <p style='font-size: 1.8rem; font-weight: bold; margin: 10px 0; color: #ffffff;'>{result}</p>\n                            <p style='font-size: 0.85rem; color: #a1a1aa; margin:0;'>
                                ⚠️ Guarda este código de 5 dígitos. Lo necesitarás para recibir transferencias de otros usuarios o del propietario de la app.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(result)

else:
    # Sidebar de usuario conectado con toques dorados
    st.sidebar.markdown(f"<h2 class='golden-title'>👋 {st.session_state.fullname}</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**Billetera ID (Código):** `{st.session_state.wallet_code}`")
    
    # Obtener el número de notificaciones pendientes
    unread_notifs = get_unread_notifications_count(st.session_state.wallet_code)
    notif_label = f"🔔 Notificaciones ({unread_notifs})" if unread_notifs > 0 else "🔔 Notificaciones"
    
    # Balance actualizado
    balance, wallet_code, balance_cop_user, is_vip_user = get_user_balance(st.session_state.username)
    st.session_state.wallet_code = wallet_code
    
    # Cálculos de balance
    balance_usd = balance * token_price_usd
    balance_cop_equiv = balance_usd * usd_cop
    
    nav_options = ["🏠 Inicio y Balance", "💸 Enviar SD", "📥 Comprar SD", "🔄 Swap y Retiros", "🛍️ Tienda Alianza", "🚚 Mensajería Alianza", notif_label, "👤 Mi Perfil", "🛡️ Términos y Seguridad"]
    
    # El checkbox de Modo Propietario ahora es exclusivo para la cuenta del propietario de la app (@admin) o wallet_code '99999'
    is_owner_user = (st.session_state.username == 'admin' or st.session_state.wallet_code == '99999' or st.session_state.is_admin)
    if is_owner_user:
        show_admin_panel = st.sidebar.checkbox("🔓 Modo Propietario (Admin)", value=st.session_state.is_admin)
        if show_admin_panel:
            if "👑 Panel del Propietario" not in nav_options:
                nav_options.append("👑 Panel del Propietario")
    elif st.session_state.is_admin:
        if "👑 Panel del Propietario" not in nav_options:
            nav_options.append("👑 Panel del Propietario")
        
    choice = st.sidebar.radio("🌐 Todas las ventanas de la app", nav_options)
    
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.fullname = None
        st.session_state.email = None
        st.session_state.wallet_code = None
        st.session_state.is_admin = False
        st.rerun()

    # --- INICIO Y BALANCE ---
    if choice == "🏠 Inicio y Balance":
        if is_vip_user == 1:
            col_title, col_vip_badge = st.columns([3, 1])
            with col_title:
                st.markdown(f"<h1 class='golden-title'>💼 Billetera de {st.session_state.fullname}</h1>", unsafe_allow_html=True)
                st.markdown("<span style='color: #ffd700; font-weight: bold; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;'>👑 ¡BIENVENIDO MIEMBRO VIP ALIANZA! Disfrutas de comisiones de retiro reducidas (1%) y ganancias de referidos al 25% de por vida.</span>", unsafe_allow_html=True)
            with col_vip_badge:
                st.image(f"data:image/jpeg;base64,{VIP_BADGE_B64}", width=110)
        else:
            st.markdown(f"<h1 class='golden-title'>💼 Billetera de {st.session_state.fullname}</h1>", unsafe_allow_html=True)
        
        # Alerta visual rápida si tiene notificaciones pendientes
        if unread_notifs > 0:
            st.info(f"📬 Tienes **{unread_notifs} nueva(s) notificación(es)** sin leer. Revísalas en la pestaña del menú lateral.")
            
        # Muestra del balance personal
        st.subheader("Balance de tu Cuenta")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="metric-title">Balance en {token['symbol']} ({token['name']})</div>
                <div class="metric-value" style="color: #10b981;">{format_num(balance)} {token['symbol']}</div>
                <div class="metric-sub">Puntos de tu cuenta</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="metric-title">Equivalente en Dólares (USD)</div>
                <div class="metric-value" style="color: #ffffff;">${balance_usd:,.2f} USD</div>
                <div class="metric-sub">Cotización: 1 {token['symbol']} = ${token_price_usd:,.4f} USD</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="metric-title">Valor Teórico en Pesos</div>
                <div class="metric-value" style="color: #ffffff;">${balance_cop_equiv:,.0f} COP</div>
                <div class="metric-sub">Tasa de Cambio: $1 USD = ${usd_cop:,.2f} COP</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="card" style="border-color: #ffd700;">
                <div class="metric-title">Saldo Retirable (COP)</div>
                <div class="metric-value" style="color: #ffd700;">${balance_cop_user:,.0f} COP</div>
                <div class="metric-sub">Saldo líquido cambiado para retiro</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Si es el Administrador, permitirle editar sus saldos directamente según su necesidad
        if st.session_state.username == 'admin' or st.session_state.wallet_code == '99999':
            st.markdown("### 🔧 Panel de Edición de Balances del Administrador")
            with st.expander("🛠️ Ajustar Mis Saldos de Administrador (Edición Directa)", expanded=True):
                st.write("Como administrador, puedes modificar tu saldo de Alianza (SD), tu saldo retirable de pesos (COP) y el Nequi oficial para recibir pagos de usuarios:")
                col_eb1, col_eb2 = st.columns(2)
                with col_eb1:
                    admin_new_sd = st.number_input("Establecer mi saldo de Alianza (SD):", value=float(balance), min_value=0.0, format="%.4f")
                    admin_new_nequi = st.text_input("Número de Cuenta NEQUI Oficial (Cuenta Madre):", value=token['nequi_number'], max_chars=11)
                with col_eb2:
                    admin_new_cop = st.number_input("Establecer mi saldo Retirable (COP):", value=float(balance_cop_user), min_value=0.0, format="%.0f")
                
                if st.button("Guardar Cambios de Saldo y Configuración", key="save_admin_balances_btn"):
                    update_user_balance_and_cop(st.session_state.wallet_code, admin_new_sd, admin_new_cop)
                    if admin_new_nequi and len(admin_new_nequi) >= 10:
                        update_global_nequi(admin_new_nequi)
                    st.success("¡Tus saldos y configuración de Nequi oficial se han actualizado con éxito!")
                    st.rerun()

        # Mercado en Vivo
        st.subheader("📊 Cotización y Mercado en Vivo")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.markdown(f"""
            <div class="card" style="border-top: 3px solid #ffd700;">
                <div class="metric-title">🪙 {token['name']} ({token['symbol']})</div>
                <div class="metric-value">${token_price_usd:,.4f} USD</div>
                <div class="metric-sub">Valor en COP: ${token_price_cop:,.2f} COP</div>
            </div>
            """, unsafe_allow_html=True)
            # Mostrar contrato
            st.caption("📜 Dirección de Contrato:")
            st.code(token['contract'], language="text")
            
        with col_c2:
            st.markdown(f"""
            <div class="card" style="border-top: 3px solid #10b981;">
                <div class="metric-title">₿ Bitcoin (BTC)</div>
                <div class="metric-value">${btc_price:,.2f} USD</div>
                <div class="metric-sub">Valor en COP: ${(btc_price*usd_cop):,.0f} COP</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("🌐 Fuente: Coinbase API (Tiempo Real)")
            
        with col_c3:
            st.markdown(f"""
            <div class="card" style="border-top: 3px solid #ffd700;">
                <div class="metric-title">💵 Tasa de Cambio (USD/COP)</div>
                <div class="metric-value">${usd_cop:,.2f} COP</div>
                <div class="metric-sub">Valor de un Dólar en Pesos</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("🏦 Fuente: AwesomeAPI (Tiempo Real)")

        # Sección de Gráficos Interactivos
        st.subheader("📈 Gráficos de Análisis e Historial")
        
        tab_user, tab_token, tab_btc, tab_cop = st.tabs([
            "💰 Historial de Mi Cuenta", 
            f"🪙 Gráfico {token['symbol']}", 
            "₿ Gráfico Bitcoin (BTC)", 
            "💵 Gráfico Dólar / Peso (COP)"
        ])
        
        with tab_user:
            df_tx = get_transaction_history(st.session_state.wallet_code)
            if len(df_tx) == 0:
                st.info("Aún no tienes movimientos en tu cuenta. Cuando recibas tokens del propietario o envíes puntos, verás tu gráfico de balance acumulado aquí.")
            else:
                # Construir historial de balance
                history_data = []
                current_bal = 0.0
                history_data.append({
                    "Fecha": "Registro Inicial",
                    "Balance (Tokens)": 0.0,
                    "Balance (USD)": 0.0,
                    "Balance (COP)": 0.0
                })
                for idx, row in df_tx.iterrows():
                    amt = row['amount']
                    if row['receiver_code'] == st.session_state.wallet_code:
                        current_bal += amt
                    else:
                        current_bal -= amt
                    
                    history_data.append({
                        "Fecha": row['timestamp'],
                        "Balance (Tokens)": current_bal,
                        "Balance (USD)": current_bal * token_price_usd,
                        "Balance (COP)": current_bal * token_price_usd * usd_cop
                    })
                
                df_hist = pd.DataFrame(history_data)
                sel_currency = st.radio("Moneda para visualizar historial de balance:", ["Tokens", "Dólares (USD)", "Pesos (COP)"], horizontal=True)
                
                y_col = "Balance (Tokens)"
                color_line = "#10b981"
                prefix = ""
                suffix = f" {token['symbol']}"
                
                if sel_currency == "Dólares (USD)":
                    y_col = "Balance (USD)"
                    color_line = "#ffffff"
                    prefix = "$"
                    suffix = " USD"
                elif sel_currency == "Pesos (COP)":
                    y_col = "Balance (COP)"
                    color_line = "#ffd700"
                    prefix = "$"
                    suffix = " COP"
                
                fig = px.line(df_hist, x="Fecha", y=y_col, markers=True, template="plotly_dark")
                fig.update_traces(line_color=color_line, line_width=3)
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis_title=f"Balance ({sel_currency})",
                    title=f"Evolución de Balance Personal en {sel_currency}"
                )
                st.plotly_chart(fig, use_container_width=True)

        with tab_token:
            # DexScreener Embed iframe interactivo de una, directamente sin textos de información redundantes
            dex_embed_html = """
            <iframe src="https://dexscreener.com/bsc/0xC324649213ec1757190bc4b78bcD41Cc1545C264?embed=1&theme=dark&trades=0" 
                    width="100%" 
                    height="600" 
                    style="border:0; border-radius: 8px;">
            </iframe>
            """
            st.components.v1.html(dex_embed_html, height=620)
            
        with tab_btc:
            st.markdown("#### ₿ Gráfico Interactivo de **Bitcoin (BTC/USD)**")
            btc_embed_html = """
            <div class="tradingview-widget-container" style="height:550px;width:100%;">
              <div id="tradingview_btc" style="height:500px;width:100%;"></div>
              <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
              <script type="text/javascript">
              new TradingView.widget({
                "autosize": true,
                "symbol": "COINBASE:BTCUSD",
                "interval": "D",
                "timezone": "Etc/UTC",
                "theme": "dark",
                "style": "1",
                "locale": "es",
                "toolbar_bg": "#f1f3f6",
                "enable_publishing": false,
                "hide_side_toolbar": false,
                "allow_symbol_change": true,
                "container_id": "tradingview_btc"
              });
              </script>
            </div>
            """
            st.components.v1.html(btc_embed_html, height=570)
            
        with tab_cop:
            st.markdown("#### Historial de la Tasa de Cambio **Dólar a Peso Colombiano (USD/COP)**")
            df_cop = get_usd_cop_historical_data()
            fig_cop = px.line(df_cop, x="Fecha", y="Tasa (COP)", markers=True, template="plotly_dark")
            fig_cop.update_traces(line_color="#ffd700", line_width=3)
            fig_cop.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_title="COP por USD"
            )
            st.plotly_chart(fig_cop, use_container_width=True)

        # Sección de Historiales de Operación Completo (Multitabs)
        st.subheader("📑 Historial Completo de Operaciones")
        
        tab_txs, tab_buys, tab_withdraws_user, tab_store_user = st.tabs([
            "💸 Envíos y Recibos",
            "📥 Compras de SD (Nequi)",
            "💰 Retiros a Nequi",
            "🛍️ Compras en Tienda"
        ])
        
        with tab_txs:
            df_tx_list = get_transaction_history(st.session_state.wallet_code)
            # Filtrar SYSTEM_STORE de las transacciones directas para no confundir al usuario (ya se ven en Compras en Tienda)
            df_tx_list = df_tx_list[df_tx_list['receiver_code'] != 'SYSTEM_STORE']
            if len(df_tx_list) > 0:
                df_disp = df_tx_list.copy()
                df_disp['Tipo'] = df_disp.apply(lambda r: "🟢 Recibido" if r['receiver_code'] == st.session_state.wallet_code else "🔴 Enviado", axis=1)
                df_disp['De'] = df_disp.apply(lambda r: "Tú (Billetera)" if r['sender_code'] == st.session_state.wallet_code else ("Owner/Sistema" if r['sender_code'] == "99999" else f"{r['sender_name']} ({r['sender_code']})"), axis=1)
                df_disp['Para'] = df_disp.apply(lambda r: "Tú (Billetera)" if r['receiver_code'] == st.session_state.wallet_code else f"{r['receiver_name']} ({r['receiver_code']})", axis=1)
                df_disp['Cantidad'] = df_disp['amount'].apply(lambda x: f"{format_num(x)} {token['symbol']}")
                df_disp['Equivalente USD'] = df_disp['amount'].apply(lambda x: f"${format_num(x * token_price_usd)} USD")
                df_disp['Equivalente COP'] = df_disp['amount'].apply(lambda x: f"${x * token_price_usd * usd_cop:,.0f} COP")
                
                df_disp = df_disp[['timestamp', 'Tipo', 'De', 'Para', 'Cantidad', 'Equivalente USD', 'Equivalente COP']]
                df_disp.columns = ['Fecha', 'Tipo', 'De/Remitente', 'Para/Destinatario', 'Monto Transado', 'Valor (USD)', 'Valor (COP)']
                st.dataframe(df_disp.iloc[::-1], use_container_width=True)
            else:
                st.info("No hay transferencias registradas todavía.")
                
        with tab_buys:
            user_purchases_df = get_user_purchases(st.session_state.wallet_code)
            if len(user_purchases_df) == 0:
                st.info("Aún no tienes solicitudes de compra de SD.")
            else:
                user_purchases_display = user_purchases_df.copy()
                user_purchases_display['Estado'] = user_purchases_display['status'].apply(
                    lambda s: "🟡 Pendiente" if s == 'PENDING' else ("🟢 Aprobada" if s == 'APPROVED' else "🔴 Rechazada")
                )
                user_purchases_display['Valor en Pesos'] = user_purchases_display['amount_cop'].apply(lambda x: f"${x:,.0f} COP")
                user_purchases_display['Tokens SD'] = user_purchases_display['amount_sd'].apply(lambda x: f"{format_num(x)} SD")
                
                for idx, r in user_purchases_display.iterrows():
                    with st.expander(f"📥 Compra #{r['id']} - {r['Fecha']} - {r['Estado']} ({r['Tokens SD']})"):
                        st.markdown(f"""
                        <p><b>Monto transferido:</b> {r['Valor en Pesos']}</p>
                        <p><b>Tokens SD solicitados:</b> {r['Tokens SD']}</p>
                        <p><b>Estado actual:</b> {r['Estado']}</p>
                        """, unsafe_allow_html=True)
                        if r['proof_image']:
                            st.markdown("<b>Tu comprobante enviado por Nequi:</b>", unsafe_allow_html=True)
                            try:
                                st.image(r['proof_image'], caption="Foto del recibo", width=250)
                            except Exception:
                                st.write("No se pudo cargar la imagen.")
                                
        with tab_withdraws_user:
            df_w_hist = get_user_withdrawals(st.session_state.wallet_code)
            if len(df_w_hist) == 0:
                st.info("No tienes solicitudes de retiros todavía.")
            else:
                for idx, row in df_w_hist.iterrows():
                    status_lbl = "🟡 Pendiente" if row['status'] == 'PENDING' else ("🟢 Pagado" if row['status'] == 'APPROVED' else "🔴 Rechazado / Reembolsado")
                    with st.expander(f"💸 Retiro #{row['id']} - {row['timestamp']} - {status_lbl} (${row['amount_cop']:,.0f} COP)"):
                        st.markdown(f"""
                        <p><b>Monto solicitado:</b> ${row['amount_cop']:,.0f} COP</p>
                        <p><b>Comisión cobrada:</b> ${row['fee_cop']:,.0f} COP</p>
                        <p><b>Neto enviado a Nequi ({row['nequi_number']}):</b> <span style="color:#10b981; font-weight:bold;">${row['net_cop']:,.0f} COP</span></p>
                        """, unsafe_allow_html=True)
                        if row['status'] == 'APPROVED' and row['receipt_image']:
                            st.markdown("<b>📸 Comprobante de pago del Administrador:</b>", unsafe_allow_html=True)
                            try:
                                st.image(row['receipt_image'], caption="Soporte de transferencia bancaria", width=250)
                            except Exception:
                                st.write("Soporte de pago no disponible.")
                                
        with tab_store_user:
            df_store_u = get_user_store_purchases(st.session_state.wallet_code)
            if len(df_store_u) == 0:
                st.info("No has realizado compras en la Tienda Alianza todavía.")
            else:
                for idx, row in df_store_u.iterrows():
                    status_lbl = "🟡 Pendiente" if row['status'] == 'PENDING' else ("🟢 Entregado" if row['status'] == 'DELIVERED' else "🔴 Cancelado / Reembolsado")
                    border_c = "#ffd700" if row['status'] == 'DELIVERED' else "#ef4444"
                    with st.expander(f"🛍️ Pedido #{row['id']} - {row['name']} - {row['timestamp']} - {status_lbl}"):
                        st.write(f"<b>Tokens gastados:</b> {row['price_sd']:,.4f} SD", unsafe_allow_html=True)
                        if row['status'] == 'DELIVERED':
                            if row['item_type'] == 'MEMBERSHIP':
                                st.success("👑 Membresía VIP activa y cargada en tu cuenta de por vida.")
                            else:
                                st.markdown(f"""
                                <div style="background-color: #0d0d11; padding: 10px; border-left: 3px solid {border_c}; margin-top:5px;">
                                    <span style="color:#ffd700; font-weight:bold;">Código/Pin de tu producto:</span>
                                    <br><code style="font-size:1.15rem; color:#ffffff;">{row['code_delivered']}</code>
                                </div>
                                """, unsafe_allow_html=True)

    # --- ENVIAR PUNTOS ---
    elif choice == "💸 Enviar SD":
        st.markdown(f"<h1 class='golden-title'>💸 Enviar {token['name']} ({token['symbol']})</h1>", unsafe_allow_html=True)
        st.write(f"Transfiere saldo de **{token['name']} ({token['symbol']})** a otro usuario de forma instantánea usando su código de billetera.")
        
        col_f, col_i = st.columns([2, 1])
        with col_f:
            with st.form("send_form"):
                rec_code = st.text_input("Código de Billetera del Destinatario (5 dígitos)", max_chars=5, placeholder="Ej. 54321")
                amount = st.number_input(f"Cantidad de {token['symbol']} a enviar", min_value=0.0001, format="%.4f")
                submit = st.form_submit_button("Confirmar Envío Directo")
                
                if submit:
                    if len(rec_code) != 5 or not rec_code.isdigit():
                        st.error("El código debe constar exactamente de 5 dígitos numéricos.")
                    elif amount <= 0:
                        st.error("El monto debe ser mayor que cero.")
                    else:
                        success, msg = send_points(st.session_state.wallet_code, rec_code, amount)
                        if success:
                            st.balloons()
                            st.success(msg)
                        else:
                            st.error(msg)
                            
        with col_i:
            st.markdown(f"""
            <div class="card" style="border-left: 5px solid #10b981;">
                <h4 style="margin-top:0; color: #ffd700;">💡 Consejos de Uso</h4>
                <ul style="padding-left: 18px; font-size: 0.9rem; color: #ffffff; line-height: 1.4rem;">
                    <li>El envío de monedas entre billeteras de esta red se efectúa en segundos.</li>\n                    <li>Por seguridad, las transacciones no son reversibles bajo ninguna circunstancia.</li>\n                    <li>Tu balance actual disponible es de <b>{format_num(balance)} {token['symbol']}</b>.</li>\n                </ul>
            </div>
            """, unsafe_allow_html=True)

            # Calculadora / Conversor dinámico para usuarios
            st.markdown(f"""
            <div class="card" style="border-left: 5px solid #ffd700;">
                <h4 style="margin-top:0; color: #ffd700; display:flex; align-items:center; gap:8px;">🧮 Conversor SIAD a Pesos</h4>
                <p style="font-size:0.85rem; color:#a1a1aa; margin-top:2px; line-height:1.2rem;">
                    Calcula cuánto valen tus tokens en Pesos Colombianos antes de transferirlos:
                </p>
            </div>
            """, unsafe_allow_html=True)

            calc_sd_input = st.number_input("Cantidad de tokens SD a cotizar:", min_value=0.0, value=100.0, step=10.0, key="send_calc_sd_input")
            calc_cop_result = calc_sd_input * token_price_cop
            calc_usd_result = calc_sd_input * token_price_usd

            st.markdown(f"""
            <div class="card" style="border-left: 5px solid #10b981; background: linear-gradient(135deg, #0d0d11 0%, #061f14 100%) !important;">
                <p style="font-size:0.85rem; color:#a1a1aa; margin: 3px 0;"><b>Monto a Enviar:</b> {format_num(calc_sd_input)} SD</p>
                <p style="font-size:0.85rem; color:#ffffff; margin: 3px 0;"><b>Equivalente en Dólares:</b> ${format_num(calc_usd_result)} USD</p>
                <p style="font-size:1.15rem; color:#ffd700; font-weight:bold; margin-top:8px; margin-bottom: 0;"><b>Equivalente en Pesos:</b> ${format_num(calc_cop_result)} COP</p>
                <span style="font-size:0.75rem; color:#888899; display:block; margin-top:8px;">Tasa actual: 1 SD = ${token_price_cop:,.2f} COP</span>
            </div>
            """, unsafe_allow_html=True)

    # --- SWAP Y RETIROS ---
    elif choice == "🔄 Swap y Retiros":
        st.markdown("<h1 class='golden-title'>🔄 Cambiar SD y Solicitar Retiro (Nequi)</h1>", unsafe_allow_html=True)
        st.write("Convierte tus tokens SIAD (SD) a pesos colombianos líquidos e inicia solicitudes de retiro seguras directamente a tu cuenta Nequi.")
        
        tab_swap, tab_withdraw, tab_history_with = st.tabs([
            "🔄 Convertir SD a Pesos (COP)", 
            "💸 Retirar COP a Nequi", 
            "📋 Historial de Retiros"
        ])
        
        with tab_swap:
            st.subheader("1. Cambiar tus Tokens SD a Pesos Colombianos")
            st.write(f"Vende tus tokens SD de forma instantánea dentro de la app para agregarlos a tu saldo retirable en pesos colombianos. Tasa de cambio oficial: **1 SD = ${token_price_cop:,.2f} COP**.")
            
            if "swap_amount" not in st.session_state:
                st.session_state.swap_amount = float(min(10.0, float(balance)))
            
            # Clamp value
            st.session_state.swap_amount = min(max(0.0, float(st.session_state.swap_amount)), float(balance))

            col_sw1, col_sw2 = st.columns([2, 1])
            with col_sw1:
                st.write("<b>💡 Selecciona un porcentaje rápido o arrastra la barra de abajo para cotización en vivo:</b>", unsafe_allow_html=True)
                col_q1, col_q2, col_q3, col_q4 = st.columns(4)
                if col_q1.button("25%", key="q_btn_25"):
                    st.session_state.swap_amount = float(balance) * 0.25
                    st.rerun()
                if col_q2.button("50%", key="q_btn_50"):
                    st.session_state.swap_amount = float(balance) * 0.50
                    st.rerun()
                if col_q3.button("75%", key="q_btn_75"):
                    st.session_state.swap_amount = float(balance) * 0.75
                    st.rerun()
                if col_q4.button("100%", key="q_btn_100"):
                    st.session_state.swap_amount = float(balance)
                    st.rerun()

                # Deslizador interactivo instantáneo para móviles
                amount_sd_to_swap_slider = st.slider(f"🎚️ Desliza para seleccionar la cantidad de {token['symbol']}:", min_value=0.0, max_value=max(float(balance), 0.0), value=float(st.session_state.swap_amount), step=1.0 if float(balance) > 10 else 0.1, key="swap_slider_key")
                st.session_state.swap_amount = amount_sd_to_swap_slider

                amount_sd_to_swap = st.number_input(f"O escribe la cantidad exacta de {token['symbol']}:", min_value=0.0000, max_value=max(float(balance), 0.0), value=float(st.session_state.swap_amount), step=1.0, format="%.4f", key="swap_amt_input_field")
                st.session_state.swap_amount = amount_sd_to_swap
                
                # Info text for mobile
                st.info("📱 <b>Tip para celular:</b> Escribe la cantidad y toca la pantalla afuera del teclado o presiona 'Hecho/Enter' para actualizar la conversión en vivo de inmediato.")

                if st.button("Ejecutar Swap de Inmediato", key="execute_swap_direct_btn"):
                    if amount_sd_to_swap <= 0:
                        st.error("⚠️ El monto a cambiar debe ser mayor que cero.")
                    elif amount_sd_to_swap > balance:
                        st.error("⚠️ Saldo de tokens SD insuficiente para realizar el swap.")
                    else:
                        success, msg = swap_sd_to_cop(st.session_state.wallet_code, amount_sd_to_swap, token_price_usd, usd_cop)
                        if success:
                            st.session_state.swap_amount = 0.0
                            st.balloons()
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
            with col_sw2:
                preview_cop_val = amount_sd_to_swap * token_price_cop
                preview_usd_val = amount_sd_to_swap * token_price_usd
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #10b981;">
                    <h4 style="margin-top:0; color:#10b981;">💰 Vista Previa de Liquidación</h4>
                    <p style="font-size:0.9rem; color:#ffffff; margin: 4px 0;"><b>Cantidad a Cambiar:</b> {format_num(amount_sd_to_swap)} SD</p>
                    <p style="font-size:0.9rem; color:#ffffff; margin: 4px 0;"><b>Equivalente en Dólares (USD):</b> ${format_num(preview_usd_val)} USD</p>
                    <p style="font-size:1.15rem; color:#ffd700; font-weight:bold; margin-top:10px;"><b>Recibirás en Pesos (COP):</b> ${format_num(preview_cop_val)} COP</p>
                    <span style="font-size:0.75rem; color:#a1a1aa; display:block; margin-top:10px;">
                        ⚠️ El cambio se efectúa con cotizaciones en tiempo real y no se puede anular ni reversar.
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
        with tab_withdraw:
            st.subheader("2. Retirar Pesos Colombianos (COP) a tu Cuenta Nequi")
            st.write("Solicita la transferencia de tu saldo acumulado en pesos a tu cuenta de ahorros Nequi. Se descuenta una tasa del **2% de comisión operacional** por procesamiento de retiro.")
            
            if balance_cop_user <= 0:
                st.info("⚠️ Tu saldo retirable está en $0 COP. Primero realiza una conversión en la pestaña 'Convertir SD a Pesos' para disponer de saldo para retiro.")
            else:
                if balance_cop_user < 1000:
                    st.warning("⚠️ El monto mínimo de retiro es de **$1,000 COP**. Tu saldo retirable actual es menor a este límite.")
                else:
                    col_w1, col_w2 = st.columns([2, 1])
                    with col_w1:
                        user_nequi_saved = get_user_nequi(st.session_state.wallet_code)
                        amount_cop_to_withdraw = st.number_input("Ingresa la cantidad en Pesos (COP) a retirar (Mínimo $1,000 COP):", min_value=1000.0, max_value=float(balance_cop_user), step=5000.0, key="withdraw_amt_input_field")
                        nequi_account_w = st.text_input("Número de Cuenta Nequi (10 dígitos):", value=user_nequi_saved, max_chars=11, placeholder="Ej. 3001234567", key="withdraw_nequi_input_field")
                        
                        st.info("📱 <b>Tip para celular:</b> Toca la pantalla fuera del teclado para actualizar el descuento de la comisión en la tarjeta de la derecha de inmediato.")

                        if st.button("Solicitar Envío de Dinero", key="submit_withdrawal_direct_btn"):
                            if amount_cop_to_withdraw < 1000:
                                st.error("El retiro mínimo es de $1,000 COP.")
                            elif amount_cop_to_withdraw > balance_cop_user:
                                st.error("No posees suficiente saldo en pesos COP retirable.")
                            elif len(nequi_account_w) < 10 or not nequi_account_w.isdigit():
                                st.error("El número de cuenta de Nequi debe constar de dígitos numéricos válidos.")
                            else:
                                success, msg = submit_withdrawal_request(st.session_state.wallet_code, amount_cop_to_withdraw, nequi_account_w)
                                if success:
                                    st.balloons()
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                with col_w2:
                    fee_pct = 0.01 if is_vip_user == 1 else 0.02
                    fee_val = amount_cop_to_withdraw * fee_pct
                    net_val = amount_cop_to_withdraw - fee_val
                    st.markdown(f"""
                    <div class="card" style="border-left: 5px solid #ffd700;">
                        <h4 style="margin-top:0; color:#ffd700;">💸 Liquidación de Transferencia</h4>
                        <p style="font-size:0.85rem; color:#ffffff;"><b>Monto de Retiro:</b> ${format_num(amount_cop_to_withdraw)} COP</p>
                        <p style="font-size:0.85rem; color:#ef4444;"><b>Comisión de Retiro ({"1%" if is_vip_user == 1 else "2%"}):</b> ${format_num(fee_val)} COP</p>
                        <hr style="border-color:#3f3f46; margin: 10px 0;">
                        <p style="font-size:1.1rem; color:#10b981; font-weight:bold;"><b>A Transferir a Nequi:</b> ${format_num(net_val)} COP</p>
                        <span style="font-size:0.75rem; color:#a1a1aa; display:block; margin-top:10px;">
                            🔒 El saldo solicitado de ${format_num(amount_cop_to_withdraw)} COP se congela para retiro y se borrará definitivamente cuando el administrador te envíe la captura de confirmación del pago.
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    
        with tab_history_with:
            st.subheader("3. Historial de Solicitudes de Retiro")
            df_w_hist = get_user_withdrawals(st.session_state.wallet_code)
            
            if len(df_w_hist) == 0:
                st.info("No hay registros de retiros solicitados todavía.")
            else:
                for idx, row in df_w_hist.iterrows():
                    status_text = "PENDIENTE" if row['status'] == 'PENDING' else ("PAGADO" if row['status'] == 'APPROVED' else "RECHAZADO")
                    status_color = "#ffd700" if row['status'] == 'PENDING' else ("#10b981" if row['status'] == 'APPROVED' else "#ef4444")
                    
                    with st.expander(f"💸 Retiro #{row['id']} - Solicitado: ${row['amount_cop']:,.0f} COP ({status_text})"):
                        col_h_info, col_h_img = st.columns([1, 1])
                        with col_h_info:
                            st.markdown(f"""
                            <div class="card" style="border-left: 3px solid {status_color};">
                                <p><b>ID de Solicitud:</b> #{row['id']}</p>
                                <p><b>Monto de Retiro COP:</b> ${row['amount_cop']:,.0f} COP</p>
                                <p><b>Comisión Operativa (2%):</b> ${row['fee_cop']:,.0f} COP</p>
                                <p><b>Monto Neto Enviado:</b> <span style="color:#10b981; font-weight:bold;">${row['net_cop']:,.0f} COP</span></p>
                                <p><b>Cuenta Nequi:</b> {row['nequi_number']}</p>
                                <p><b>Estado:</b> <span style="color:{status_color}; font-weight:bold;">{status_text}</span></p>
                                <p><b>Fecha de Solicitud:</b> {row['timestamp']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_h_img:
                            if row['status'] == 'APPROVED' and row['receipt_image']:
                                st.subheader("📷 Comprobante de Pago")
                                try:
                                    st.image(row['receipt_image'], caption="Foto del soporte de transferencia Nequi oficial cargada por el admin", use_container_width=True)
                                except Exception:
                                    st.error("No se pudo cargar la imagen del comprobante.")
                            elif row['status'] == 'PENDING':
                                st.info("⏳ Solicitud recibida. El administrador está realizando el pago a tu cuenta Nequi. Una vez realizado, aparecerá tu comprobante aquí.")
                            else:
                                st.error("❌ Retiro rechazado. Los fondos regresaron a tu saldo retirable.")

    # --- COMPRAR SD (PROOF OF PAYMENT & NEQUI) ---
    elif choice == "📥 Comprar SD":
        st.markdown(f"<h1 class='golden-title'>📥 Adquirir Tokens {token['symbol']}</h1>", unsafe_allow_html=True)
        st.write("Sigue los pasos detallados a continuación para recargar saldo de forma directa y oficial.")
        
        col_calc, col_nequi = st.columns([3, 2])
        
        with col_nequi:
            st.markdown(f"""
            <div class="card" style="border-left: 5px solid #ffd700;">
                <h4 style="margin-top:0; color: #ffd700; display: flex; align-items: center; gap: 8px;">📲 Paso 1: Transfiere por NEQUI</h4>\n                <p style="font-size: 0.9rem; color: #e2e8f0; line-height: 1.4rem;">
                    Realiza tu pago desde la app Nequi al número oficial del administrador.
                    <b>Toca el número abajo para seleccionarlo y copiarlo de inmediato:</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.code(token['nequi_number'], language="text")
            
            st.markdown(f"""
            <div class="card" style="border-top: 2px solid #10b981;">
                <h5 style="color: #ffd700; margin-top:0;">📋 Requisitos para el Proceso</h5>\n                <ul style="padding-left: 18px; font-size: 0.85rem; color: #a1a1aa; line-height: 1.3rem;">
                    <li>Conserva una captura de pantalla clara de tu comprobante con hora e ID de transacción.</li>\n                    <li>El sistema autodetectará tu dirección de billetera (ID): <code style="color: #10b981;">{st.session_state.wallet_code}</code>.</li>\n                    <li>Una vez verificado, tu saldo se actualizará automáticamente.</li>\n                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col_calc:
            st.subheader("Paso 2: Cotiza tu compra")
            amount_cop_input = st.number_input("Ingresa la cantidad en Pesos Colombianos (COP) que vas a transferir:", min_value=1000, value=20000, step=5000)
            
            sd_to_receive = amount_cop_input / token_price_cop
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.markdown(f"""
                <div class="card" style="border-color: #ffd700;">
                    <div class="metric-title">Monto a pagar (COP)</div>
                    <div class="metric-value" style="color: #ffd700;">${amount_cop_input:,.0f} COP</div>
                </div>
                """, unsafe_allow_html=True)
            with col_c2:
                st.markdown(f"""
                <div class="card" style="border-color: #10b981;">
                    <div class="metric-title">Tokens a recibir ({token['symbol']})</div>
                    <div class="metric-value" style="color: #10b981;">{sd_to_receive:,.4f} SD</div>
                    <div class="metric-sub">Tasa: 1 SD = ${token_price_cop:,.2f} COP</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.subheader("Paso 3: Sube tu Comprobante de Pago")
            uploaded_file = st.file_uploader("Adjunta la imagen/foto de tu transferencia Nequi:", type=["png", "jpg", "jpeg"])
            
            if st.button("Enviar Solicitud de Compra"):
                if not uploaded_file:
                    st.error("⚠️ Debes adjuntar la imagen del comprobante para que el administrador pueda procesar tu compra.")
                else:
                    try:
                        img_bytes = uploaded_file.read()
                        submit_purchase_request(st.session_state.wallet_code, amount_cop_input, sd_to_receive, img_bytes)
                        st.balloons()
                        st.success("🎉 ¡Tu comprobante ha sido enviado con éxito al administrador! Tu compra de " + f"{sd_to_receive:,.4f} SD" + " está siendo procesada.")
                    except Exception as e:
                        st.error(f"Error procesando la solicitud: {str(e)}")

    # --- PESTAÑA: NOTIFICACIONES ---
    elif "Notificaciones" in choice:
        st.markdown("<h1 class='golden-title'>🔔 Bandeja de Notificaciones</h1>", unsafe_allow_html=True)
        st.write("Mantente al tanto de la aprobación de tus transacciones, recargas de saldo y actualizaciones del sistema.")
        
        # Marcar todas como leídas al entrar
        mark_notifications_as_read(st.session_state.wallet_code)
        
        notifs_df = get_user_notifications(st.session_state.wallet_code)
        
        if len(notifs_df) == 0:
            st.info("No tienes notificaciones registradas en tu historial.")
        else:
            for idx, row in notifs_df.iterrows():
                # Formato y estilo de la tarjeta de notificación
                border_color = "#ffd700"
                if "aprobada" in row['message'] or "recibido" in row['message']:
                    border_color = "#10b981"
                elif "rechazada" in row['message']:
                    border_color = "#ef4444"
                
                # Renderizar HTML limpio para cada notificación
                st.markdown(f"""
                <div class="notification-card" style="border-left-color: {border_color} !important;">
                    <span style="font-size: 0.8rem; color: #888899; float: right;">{row['timestamp']}</span>
                    <p style="margin: 0; font-size: 0.95rem; line-height: 1.4rem; color: #ffffff;">{row['message']}</p>
                </div>
                """, unsafe_allow_html=True)

    # --- TIENDA Alianza (COMPRA DE ARTÍCULOS Y MEMBRESÍA VIP) ---
    elif choice == "🛍️ Tienda Alianza":
        st.markdown(f"<h1 class='golden-title'>🛍️ Tienda Oficial Alianza ({token['symbol']})</h1>", unsafe_allow_html=True)
        st.write("Gasta tus tokens SIAD (SD) acumulados en entretenimiento, recargas de juegos o adquiere la membresía VIP para maximizar tus ganancias financieras.")
        
        # Consultar si el usuario es VIP
        is_vip_val = is_vip_user == 1
        
        # Tarjeta VIP de estado del usuario
        if is_vip_val:
            st.markdown("""
            <div class="card" style="border-left: 5px solid #10b981; background: linear-gradient(135deg, #0d0d11 0%, #061f14 100%) !important;">
                <h4 style="color: #10b981; margin:0; display:flex; align-items:center; gap:8px;">👑 MIEMBRO VIP DE Alianza</h4>
                <p style="font-size:0.9rem; margin-top:5px; color:#ffffff; line-height:1.4rem;">
                    ¡Felicidades! Tienes activos tus beneficios VIP permanentes:
                    <br>• Comisión de Retiro a Nequi reducida al <b>1%</b> (en lugar de 2%).
                    <br>• Comisión de Referidos aumentada al <b>25%</b> (en lugar de 20%).
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card" style="border-left: 5px solid #ffd700;">
                <h4 style="color: #ffd700; margin:0;">🌟 ¿Quieres maximizar tus ganancias?</h4>
                <p style="font-size:0.9rem; margin-top:5px; color:#a1a1aa; line-height:1.4rem;">
                    Adquiere la <b>Membresía VIP Alianza</b> en el catálogo de abajo para bajar tus tasas de retiro a la mitad y cobrar comisiones más altas por tus invitados.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        # Catálogo de Artículos
        st.subheader("🛒 Catálogo de Artículos y Membresías")
        
        conn = get_db_connection()
        items_df = pd.read_sql_query("SELECT id, name, description, price_sd, item_type FROM store_items", conn)
        conn.close()
        
        col_item_cards = st.columns(3)
        for idx, row in items_df.iterrows():
            col_idx = idx % 3
            with col_item_cards[col_idx]:
                border_color = "#ffd700" if row['item_type'] == 'MEMBERSHIP' else "#10b981"
                btn_label = "Adquirir Membresía" if row['item_type'] == 'MEMBERSHIP' else f"Comprar Pin"
                
                # Deshabilitar si ya es VIP
                is_disabled = row['item_type'] == 'MEMBERSHIP' and is_vip_val
                
                st.markdown(f"""
                <div class="card" style="border-color: {border_color}; min-height: 240px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <h4 style="color: {border_color}; margin-top:0;">{row['name']}</h4>
                        <p style="font-size:0.85rem; color:#e2e8f0; line-height: 1.3rem; min-height: 60px;">{row['description']}</p>
                    </div>
                    <div style="margin-top: 15px;">
                        <span style="font-size: 1.3rem; font-weight: 800; color: #ffffff;">{row['price_sd']:,.2f} SD</span>
                        <span style="font-size: 0.8rem; color: #a1a1aa; display:block;">Equivale aprox. a ${(row['price_sd'] * token_price_cop):,.0f} COP</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if is_disabled:
                    st.button("👑 VIP Ya Adquirido", key=f"buy_btn_{row['id']}", disabled=True)
                else:
                    if st.button(f"{btn_label} - {row['price_sd']} SD", key=f"buy_btn_{row['id']}"):
                        success, msg = buy_store_item(st.session_state.wallet_code, row['id'])
                        if success:
                            st.balloons()
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

    # --- SECCIÓN: COURIER Y CONDUCTORES (MENSAJERÍA Alianza) ---
    elif choice == "🚚 Mensajería Alianza":
        st.markdown("<h1 class='golden-title'>🚚 Servicios de Mensajería y Móviles</h1>", unsafe_allow_html=True)
        st.write("Gestiona los pagos de envíos de encomiendas de forma directa y cancela tus cuotas semanales de móviles con descuentos especiales en tokens SD.")
        
        tab_pay_ship, tab_pay_fee, tab_ship_history = st.tabs([
            "📦 Pagar Servicio de Envío",
            "💳 Pagar Cuota Semanal (Móviles)",
            "📋 Mi Historial de Mensajería"
        ])
        
        with tab_pay_ship:
            st.subheader("Pagar Envío Directamente al Conductor")
            st.write("Ingresa el código único del móvil para transferirle de forma segura el valor del envío en tokens SIAD (SD).")
            
            col_ship_f, col_ship_info = st.columns([2, 1])
            with col_ship_f:
                driver_code_input = st.text_input("Código de Billetera del Conductor / Móvil (5 dígitos):", max_chars=5, placeholder="Ej. 12345", key="msg_driver_input_field")
                
                if "msg_amt_input" not in st.session_state:
                    st.session_state.msg_amt_input = 5.0
                
                st.write("<b>💡 Tarifas rápidas o desliza la barra de abajo para cotización en vivo:</b>", unsafe_allow_html=True)
                col_sh_b1, col_sh_b2, col_sh_b3, col_sh_b4 = st.columns(4)
                if col_sh_b1.button("5 SD", key="sh_btn_5"):
                    st.session_state.msg_amt_input = 5.0
                    st.rerun()
                if col_sh_b2.button("10 SD", key="sh_btn_10"):
                    st.session_state.msg_amt_input = 10.0
                    st.rerun()
                if col_sh_b3.button("15 SD", key="sh_btn_15"):
                    st.session_state.msg_amt_input = 15.0
                    st.rerun()
                if col_sh_b4.button("20 SD", key="sh_btn_20"):
                    st.session_state.msg_amt_input = 20.0
                    st.rerun()

                # Deslizador interactivo instantáneo para celular
                amount_sd_input_slider = st.slider("🎚️ Desliza para ajustar la tarifa del envío:", min_value=0.0, max_value=200.0, value=float(st.session_state.msg_amt_input), step=1.0, key="msg_amt_slider_key")
                st.session_state.msg_amt_input = amount_sd_input_slider

                amount_sd_input = st.number_input("O escribe el monto exacto en Tokens SD:", min_value=0.0000, value=float(st.session_state.msg_amt_input), step=1.0, format="%.4f", key="msg_amt_input_field")
                st.session_state.msg_amt_input = amount_sd_input
                service_id_input = st.text_input("ID de Envío / Número de Guía (Opcional):", placeholder="Ej. GUIA-9831", key="msg_guia_input_field")
                
                st.info("📱 <b>Tip para celular:</b> Toca la pantalla fuera del teclado para actualizar la cotización de subsidio de la derecha de inmediato.")

                if st.button("Confirmar y Pagar Envío", key="pay_delivery_direct_btn"):
                    if len(driver_code_input) != 5 or not driver_code_input.isdigit():
                        st.error("⚠️ El código del móvil debe tener exactamente 5 dígitos numéricos.")
                    elif amount_sd_input <= 0:
                        st.error("⚠️ El monto del pago en SD debe ser mayor a cero.")
                    else:
                        success, msg = pay_delivery_service(st.session_state.wallet_code, driver_code_input, amount_sd_input, service_id_input)
                        if success:
                            st.balloons()
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
            with col_ship_info:
                # Mostrar cotización del envío dinámicamente
                equiv_cop_calc = amount_sd_input * token_price_cop
                cashback_sd_preview = amount_sd_input * 0.5
                cashback_cop_preview = equiv_cop_calc * 0.5
                net_sd_preview = amount_sd_input * 0.5
                net_cop_preview = equiv_cop_calc * 0.5
                driver_receives_sd = amount_sd_input * 1.1
                driver_receives_cop = equiv_cop_calc * 1.1
                
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #10b981; background: linear-gradient(135deg, #000000 0%, #061f14 100%) !important;">
                    <h4 style="margin-top:0; color:#10b981; display:flex; align-items:center; gap:8px;">🔥 ¡Subsidio Alianza Activo!</h4>
                    <p style="font-size:0.85rem; color:#a1a1aa; margin-top:2px; line-height:1.2rem;">
                        Al pagar tu envío usando tus tokens <b>Alianza (SD)</b>, el Administrador financia automáticamente el <b>50%</b> de tu envío y te lo devuelve al instante.
                    </p>
                    <hr style="border-color:#232d42; margin: 10px 0;">
                    <p style="font-size:0.85rem; color:#ffffff; margin:3px 0;"><b>Tarifa de Envío:</b> {format_num(amount_sd_input)} SD (${format_num(equiv_cop_calc)} COP)</p>
                    <p style="font-size:0.85rem; color:#10b981; margin:3px 0;"><b>Cashback al Instante (50%):</b> +{format_num(cashback_sd_preview)} SD (+${format_num(cashback_cop_preview)} COP)</p>
                    <p style="font-size:1.1rem; color:#ffd700; font-weight:bold; margin:8px 0;"><b>Tu Costo Neto Real:</b> {format_num(net_sd_preview)} SD (${format_num(net_cop_preview)} COP)</p>
                    <hr style="border-color:#232d42; margin: 10px 0;">
                    <p style="font-size:0.85rem; color:#ffffff; margin:3px 0;"><b>El Conductor recibe (110%):</b></p>
                    <p style="font-size:1.0rem; color:#10b981; font-weight:bold; margin:3px 0;">{format_num(driver_receives_sd)} SD (${format_num(driver_receives_cop)} COP)</p>
                    <span style="font-size:0.75rem; color:#a1a1aa; line-height:1.1rem; display:block; margin-top:10px;">
                        ℹ️ El 50% de tu reembolso y el 10% de bono del conductor son financiados automáticamente de forma directa desde la billetera de fondos base del administrador.
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
        with tab_pay_fee:
            st.subheader("Pago de Cuota Semanal para Móviles")
            st.write("Si conduces un móvil afiliado a la red de mensajería, debes pagar tu cuota semanal obligatoria de **$40,000 COP**.")
            st.markdown("""
            <div class="card" style="border-left: 5px solid #ffd700; background: linear-gradient(135deg, #0d0d11 0%, #201a00 100%) !important;">
                <h4 style="color:#ffd700; margin:0;">🔥 ¡Paga con Tokens SD y Obtén un 20% de Descuento!</h4>
                <p style="font-size:0.9rem; margin-top:5px; color:#ffffff; line-height:1.4rem;">
                    Si decides pagar tu cuota semanal usando tus tokens <b>Alianza (SD)</b>, el valor se reduce automáticamente a <b>$32,000 COP</b>.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Input de mensaje de reporte del usuario
            fee_message = st.text_input("💬 Mensaje o reporte de pago opcional (Ej: Pago movil Jorge):", placeholder="Ej: Pago movil Jorge", key="weekly_fee_msg_text_field")
            
            fee_cop_with_discount = 32000.0
            fee_cop_normal = 40000.0
            
            fee_sd_with_discount = fee_cop_with_discount / token_price_cop
            
            col_fee_1, col_fee_2 = st.columns(2)
            
            with col_fee_1:
                st.markdown(f"""
                <div class="card" style="border-color: #10b981; min-height: 280px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <h4 style="color:#10b981; margin-top:0;">🪙 Opción A: Pago con Tokens SD</h4>
                        <p style="font-size:0.85rem; color:#a1a1aa;">Paga con tus monedas ganadas o compradas y aprovecha el descuento de tarifa.</p>
                        <hr style="border-color:#232d42; margin:10px 0;">
                        <span style="font-size:0.9rem; color:#ffffff;"><b>Valor cuota:</b> $32,000 COP (20% OFF)</span><br>
                        <span style="font-size:1.35rem; font-weight:800; color:#ffd700; display:block; margin-top:5px;">{format_num(fee_sd_with_discount)} SD</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Pagar Cuota con SD", key="pay_fee_sd_btn"):
                    success, msg = pay_weekly_fee(st.session_state.wallet_code, use_tokens=True, message=fee_message)
                    if success:
                        st.balloons()
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
            with col_fee_2:
                st.markdown(f"""
                <div class="card" style="border-color: #ffd700; min-height: 280px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <h4 style="color:#ffd700; margin-top:0;">💵 Opción B: Pago con Saldo Pesos (COP)</h4>
                        <p style="font-size:0.85rem; color:#a1a1aa;">Debita directamente de tu saldo retirable en pesos disponible en la app.</p>
                        <hr style="border-color:#232d42; margin:10px 0;">
                        <span style="font-size:0.9rem; color:#ffffff;"><b>Valor cuota:</b> $40,000 COP (Sin descuento)</span><br>
                        <span style="font-size:1.35rem; font-weight:800; color:#ffffff; display:block; margin-top:5px;">${fee_cop_normal:,.0f} COP</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Pagar Cuota con Saldo COP", key="pay_fee_cop_btn"):
                    success, msg = pay_weekly_fee(st.session_state.wallet_code, use_tokens=False, message=fee_message)
                    if success:
                        st.balloons()
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
        with tab_ship_history:
            st.subheader("Historial de Operaciones de Mensajería")
            st.write("Consulta el registro de pagos de envíos realizados, recibidos y pagos de cuotas semanales de móviles.")
            
            df_m_hist = get_movil_payments_history(st.session_state.wallet_code)
            
            if len(df_m_hist) == 0:
                st.info("Aún no tienes registros de mensajería registrados.")
            else:
                df_m_display = df_m_hist.copy()
                
                df_m_display['Tipo de Pago'] = df_m_display['payment_type'].apply(
                    lambda t: "📦 Pago de Envío" if t == 'SHIPPING_PAYMENT' 
                    else ("💳 Cuota Semanal (SD)" if t == 'WEEKLY_FEE_SD' else "💳 Cuota Semanal (COP)")
                )
                
                df_m_display['Rol'] = df_m_display.apply(
                    lambda r: "Remitente/Cliente" if r['target_code'] == '99999' or r['target_code'] != st.session_state.wallet_code else "Receptor/Conductor", axis=1
                )
                
                df_m_display['De'] = df_m_display.apply(
                    lambda r: "Tú" if r['customer_name'] == st.session_state.fullname else f"{r['customer_name']}", axis=1
                )
                df_m_display['Para/Destino'] = df_m_display.apply(
                    lambda r: "Maestra / Admin" if r['target_code'] == '99999' else (f"{r['driver_name']}" if r['target_code'] == st.session_state.wallet_code else f"{r['driver_name']} ({r['target_code']})"), axis=1
                )
                
                df_m_display['Tokens SD'] = df_m_display['amount_sd'].apply(lambda x: f"{format_num(x)} SD")
                df_m_display['Pesos Colombianos'] = df_m_display['amount_cop'].apply(lambda x: f"${x:,.0f} COP")
                df_m_display['Mensaje'] = df_m_display['message'].apply(lambda x: str(x) if x else "Ninguno")
                
                df_m_display = df_m_display[['timestamp', 'Tipo de Pago', 'Rol', 'De', 'Para/Destino', 'Tokens SD', 'Pesos Colombianos', 'Mensaje']]
                df_m_display.columns = ['Fecha/Hora', 'Tipo de Operación', 'Tu Rol', 'Emisor/Cliente', 'Receptor/Destinatario', 'Tokens SD', 'Pesos Colombianos', 'Mensaje/Detalle']
                st.dataframe(df_m_display, use_container_width=True)


    # --- PERFIL ---
    elif choice == "👤 Mi Perfil":
        st.markdown("<h1 class='golden-title'>👤 Configuración de Perfil</h1>", unsafe_allow_html=True)
        col_prof, col_pwd = st.columns(2)
        with col_prof:
            # Si el usuario es VIP, mostrar insignia llamativa
            if is_vip_user == 1:
                st.markdown("""
                <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px; background: linear-gradient(135deg, #201a00 0%, #0d0d11 100%) !important; padding: 15px; border-radius: 12px; border: 1px solid #ffd700;">
                    <div style="flex-shrink: 0;">
                """, unsafe_allow_html=True)
                st.image(f"data:image/jpeg;base64,{VIP_BADGE_B64}", width=70)
                st.markdown("""
                    </div>
                    <div>
                        <h3 style="margin: 0; color: #ffd700; font-weight: 800; font-size: 1.25rem;">👑 MIEMBRO VIP ALIANZA</h3>
                        <p style="margin: 4px 0 0 0; color: #ffffff; font-size: 0.85rem; line-height: 1.2rem;">Comisiones de retiro del 1% y ganancias de referidos del 25% de por vida.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card">
                <h3 style="margin-top:0; color: #ffd700;">📋 Información de Cuenta</h3>\n                <hr style="border-color: #ffd700; margin: 15px 0;">\n                <p><b>Nombre Completo:</b> {st.session_state.fullname}</p>\n                <p><b>Usuario:</b> {st.session_state.username}</p>\n                <p><b>Correo Electrónico:</b> {st.session_state.email}</p>\n                <p><b>Billetera ID (Inmutable):</b> <code style="font-size: 1.15rem; color:#10b981;">{st.session_state.wallet_code}</code></p>\n                <hr style="border-color: #232d42; margin: 15px 0;">\n                <p style="font-size:0.9rem; color:#ffd700;"><b>¿Necesitas más tokens?</b></p>\n                <p style="font-size:0.85rem; color:#a1a1aa; margin-bottom:15px;">Puedes adquirir tokens directamente haciendo una transferencia e ingresando tu comprobante de pago.</p>\n            </div>
            """, unsafe_allow_html=True)
            
            # Formulario dinámico para guardar y actualizar el Nequi del propio usuario o del administrador (cuenta madre)
            user_nequi_val = get_user_nequi(st.session_state.wallet_code)
            is_admin_user = (st.session_state.username == 'admin' or st.session_state.wallet_code == '99999')
            with st.form("edit_nequi_form"):
                if is_admin_user:
                    st.write("<b>📱 Nequi Oficial de Recaudación (Cuenta Madre)</b>", unsafe_allow_html=True)
                    new_user_nequi = st.text_input("Ingresa el número de Nequi oficial para recibir pagos de usuarios:", value=token['nequi_number'], max_chars=11, placeholder="Ej. 3001234567")
                else:
                    st.write("<b>📱 Mi Cuenta de Nequi</b>", unsafe_allow_html=True)
                    new_user_nequi = st.text_input("Ingresa tu número de celular Nequi para recibir retiros:", value=user_nequi_val, max_chars=11, placeholder="Ej. 3001234567")
                
                submit_nequi = st.form_submit_button("Guardar Nequi")
                
                if submit_nequi:
                    if new_user_nequi and (len(new_user_nequi) < 10 or not new_user_nequi.isdigit()):
                        st.error("⚠️ Por favor ingresa un número de Nequi válido de 10 dígitos.")
                    else:
                        if is_admin_user:
                            update_global_nequi(new_user_nequi)
                            st.success("✅ ¡El Nequi de recaudación oficial (Cuenta Madre) ha sido actualizado!")
                        else:
                            update_user_nequi(st.session_state.wallet_code, new_user_nequi)
                            st.success("✅ ¡Tu cuenta de Nequi ha sido actualizada!")
                        st.rerun()
            
            if st.button("Ir a Comprar SD"):
                st.info("Utiliza la barra lateral e ingresa al menú '📥 Comprar SD'")
            
        with col_pwd:
            st.subheader("🔒 Cambiar Contraseña")
            with st.form("pwd_form"):
                o_pwd = st.text_input("Contraseña Actual", type="password")
                n_pwd = st.text_input("Nueva Contraseña", type="password")
                c_pwd = st.text_input("Confirmar Nueva Contraseña", type="password")
                sub_p = st.form_submit_button("Actualizar Contraseña")
                
                if sub_p:
                    if not (o_pwd and n_pwd and c_pwd):
                        st.warning("Todos los campos son obligatorios.")
                    elif n_pwd != c_pwd:
                        st.error("Las nuevas contraseñas no coinciden.")
                    elif len(n_pwd) < 6:
                        st.error("La nueva contraseña debe tener al menos 6 caracteres.")
                    else:
                        succ, msg = change_user_password(st.session_state.username, o_pwd, n_pwd)
                        if succ:
                            st.success(msg)
                        else:
                            st.error(msg)

    # --- PESTAÑA: TÉRMINOS Y SEGURIDAD ---
    elif choice == "🛡️ Términos y Seguridad":
        st.markdown("<h1 class='golden-title'>🛡️ Términos, Condiciones y Seguridad</h1>", unsafe_allow_html=True)
        st.write("Revisa las políticas, normativas e instructivos de seguridad operacional para interactuar con la red oficial Alianza.")
        
        col_terms, col_sec = st.columns(2)
        
        with col_terms:
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #ffd700;">
                <h3 style="margin-top:0; color: #ffd700;">📝 Términos y Condiciones</h3>\n                <hr style="border-color: #ffd700; margin: 10px 0;">\n                <ol style="padding-left: 18px; font-size: 0.9rem; color: #e2e8f0; line-height: 1.5rem;">
                    <li><b>Naturaleza del Token:</b> La moneda digital SIAD (SD) opera de forma descentralizada y segura en nuestra plataforma privada. La posesión de SD representa la total conformidad con el reglamento general.</li>\n                    <li><b>Irreversibilidad de Transacciones:</b> Debido a la estructura criptográfica e inmutabilidad de la base de datos de Alianza, <b>todas las transacciones, transferencias y envíos son definitivos</b>. No existe la posibilidad de reverso, anulación o cancelación.</li>\n                    <li><b>Responsabilidad de Envío:</b> Es responsabilidad exclusiva y total del usuario remitente verificar el código único de billetera de 5 dígitos del destinatario antes de presionar el botón de envío.</li>\n                    <li><b>Veracidad de los Pagos:</b> El envío de capturas o comprobantes de pago alterados, falsos o de transacciones ya procesadas resultará en la suspensión inmediata y permanente de la cuenta del usuario sin derecho a reclamos.</li>\n                </ol>
            </div>
            """, unsafe_allow_html=True)
            
        with col_sec:
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #10b981;">
                <h3 style="margin-top:0; color: #10b981;">🔒 Estándar y Políticas de Seguridad</h3>\n                <hr style="border-color: #10b981; margin: 10px 0;">\n                <ul style="padding-left: 18px; font-size: 0.9rem; color: #e2e8f0; line-height: 1.5rem; list-style-type: square;">
                    <li><b>Criptografía de Contraseñas:</b> Su contraseña está protegida por un sistema de Hashing <b>SHA-256 de nivel bancario</b>. Nadie, ni siquiera los administradores de la plataforma, tiene acceso a ver o recuperar su clave en texto plano.</li>\n                    <li><b>Código ID Inmutable:</b> Tu identificador único de billetera de 5 dígitos se genera de manera criptográfica al momento del registro. Este código es <b>permanente, inmutable y de por vida</b>. No se puede modificar bajo ningún motivo técnico.</li>\n                    <li><b>Cierre de Sesión Seguro:</b> Recuerda que tu sesión permanece abierta mientras uses tu navegador. Si accedes a la billetera desde computadores compartidos o públicos, asegúrate de utilizar el botón <b>Cerrar Sesión</b> de la barra lateral para evitar accesos no autorizados.</li>\n                    <li><b>Soporte Oficial:</b> Los administradores nunca te pedirán tu contraseña de acceso para verificar saldos o realizar aprobaciones de comprobantes de pago.</li>\n                </ul>
            </div>
            """, unsafe_allow_html=True)

    # --- PANEL DEL PROPIETARIO ---
    elif choice == "👑 Panel del Propietario":
        st.markdown("<h1 class='golden-title'>👑 Consola del Propietario de la App</h1>", unsafe_allow_html=True)
        
        pending_claims_count = len(get_pending_purchases())
        pending_rewards_count = len(get_pending_referral_rewards())
        pending_withdraws_count = len(get_pending_withdrawals())
        pending_store_count = len(get_pending_store_purchases())
        
        tab_mint, tab_claims, tab_withdraws, tab_store, tab_referrals, tab_fees, tab_messenger, tab_broadcast, tab_settings = st.tabs([
            "💸 Emisión de Monedas", 
            f"📥 Comprobantes por Confirmar ({pending_claims_count})", 
            f"💰 Solicitudes de Retiro ({pending_withdraws_count})",
            f"🛍️ Pedidos de Tienda ({pending_store_count})",
            f"👥 Comisiones de Referidos ({pending_rewards_count})",
            "📊 Comisiones de Plataforma",
            "🚚 Control de Mensajería",
            "📢 Enviar Comunicado",
            "⚙️ Configuración del Token y Nequi"
        ])
        
        with tab_mint:
            st.subheader("💸 Cargar Monedas Directamente")
            st.write("Acredita saldo directamente ingresando el código de billetera.")
            
            conn = get_db_connection()
            users_df = pd.read_sql_query("""
                SELECT fullname as 'Nombre', username as 'Usuario', wallet_code as 'Código de Billetera', balance as 'Balance actual (SD)'
                FROM users 
                WHERE is_admin = 0
            """, conn)
            conn.close()
            
            if len(users_df) == 0:
                st.info("No hay usuarios registrados todavía.")
            else:
                st.dataframe(users_df, use_container_width=True)
                
                with st.form("mint_form"):
                    t_code = st.text_input("Ingresa el código de 5 dígitos del destinatario", max_chars=5, placeholder="Ej. 12345")
                    m_amount = st.number_input(f"Monto de {token['symbol']} a emitir y transferir", min_value=0.0001, step=100.0, format="%.4f")
                    submit_m = st.form_submit_button("Acreditar Billetera")
                    
                    if submit_m:
                        if len(t_code) != 5 or not t_code.isdigit():
                            st.error("El código debe ser de exactamente 5 dígitos numéricos.")
                        else:
                            succ, msg = send_points("99999", t_code, m_amount)
                            if succ:
                                # Enviar notificación directa por asignación manual
                                add_notification(
                                    t_code,
                                    f"👑 <b>¡Acreditación Oficial!</b> El propietario de la app ha cargado directamente "
                                    f"<b>{format_num(m_amount)} SD</b> en tu cuenta."
                                )
                                st.success(f"¡Asignación Exitosa! Se enviaron {format_num(m_amount)} {token['symbol']} al código {t_code}.")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(msg)
            
            st.markdown("---")
            st.subheader("👑 Gestión y Activación Manual de Membresía VIP")
            st.write("Como propietario, puedes otorgar o remover directamente el estado VIP de cualquier usuario:")
            with st.form("manual_vip_form"):
                vip_wallet_code = st.text_input("Código de Billetera del Usuario (5 dígitos):", max_chars=5, placeholder="Ej. 12345")
                action_vip = st.selectbox("Acción a ejecutar:", ["Activar Membresía VIP (1% Comisión)", "Desactivar Membresía VIP (2% Comisión)"])
                submit_vip_btn = st.form_submit_button("Ejecutar Acción VIP")
                
                if submit_vip_btn:
                    if len(vip_wallet_code) != 5 or not vip_wallet_code.isdigit():
                        st.error("⚠️ El código de billetera debe constar exactamente de 5 dígitos numéricos.")
                    else:
                        is_enable = "Activar" in action_vip
                        success_v, msg_v = toggle_user_vip_manually(vip_wallet_code, is_enable)
                        if success_v:
                            st.success(msg_v)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(msg_v)
                                
        with tab_claims:
            st.subheader("📥 Verificación Manual de Comprobantes de Nequi")
            st.write("Revisa los recibos enviados por los usuarios. Verifica en tu Nequi personal antes de aprobar la acreditación.")
            
            claims_df = get_pending_purchases()
            
            if len(claims_df) == 0:
                st.info("🎉 ¡Al día! No hay comprobantes de pago pendientes de verificación.")
            else:
                for idx, row in claims_df.iterrows():
                    with st.expander(f"📥 Solicitud #{row['id']} - Usuario: {row['fullname']} ({row['user_code']})"):
                        col_req_info, col_req_image = st.columns([1, 1])
                        
                        with col_req_info:
                            st.markdown(f"""
                            <div class="card" style="border-left: 3px solid #ffd700;">
                                <p><b>Usuario:</b> {row['fullname']} (@{row['username']})</p>\n                                <p><b>Código de Billetera:</b> <code style="color:#10b981;">{row['user_code']}</code></p>\n                                <p><b>Cantidad de Dinero Transferido:</b> <span style="color:#ffd700; font-weight:bold;">${row['amount_cop']:,.0f} COP</span></p>\n                                <p><b>Tokens SD a Acreditar:</b> <span style="color:#10b981; font-weight:bold;">{row['amount_sd']:,.4f} SD</span></p>\n                                <p><b>Fecha de Solicitud:</b> {row['timestamp']}</p>\n                            </div>
                            """, unsafe_allow_html=True)
                            
                            col_app, col_app_vip, col_rej = st.columns(3)
                            with col_app:
                                if st.button("Confirmar Compra (Tokens SD)", key=f"app_{row['id']}"):
                                    success, msg = approve_purchase(row['id'])
                                    if success:
                                        st.success("¡Transacción aprobada y tokens acreditados!")
                                        st.rerun()
                                    else:
                                        st.error(msg)
                            with col_app_vip:
                                if st.button("👑 Confirmar como VIP", key=f"app_vip_{row['id']}"):
                                    success, msg = approve_purchase_as_vip(row['id'])
                                    if success:
                                        st.success("¡Membresía VIP aprobada y activada con éxito!")
                                        st.rerun()
                                    else:
                                        st.error(msg)
                            with col_rej:
                                if st.button("Rechazar Solicitud", key=f"rej_{row['id']}"):
                                    if reject_purchase(row['id']):
                                        st.warning("Solicitud de pago rechazada.")
                                        st.rerun()
                                        
                        with col_req_image:
                            st.subheader("📷 Comprobante Recibido")
                            try:
                                # Mostrar la imagen BLOB guardada en la base de datos
                                st.image(row['proof_image'], caption="Foto del recibo de Nequi subida por el usuario", use_container_width=True)
                            except Exception as e:
                                st.error(f"No se pudo cargar la imagen del comprobante: {str(e)}")
                                
        with tab_withdraws:
            st.subheader("💰 Validación y Pago Manual de Retiros a Nequi")
            st.write("Revisa las solicitudes de retiro en pesos (COP). Transfiere el **Monto Neto** al número de Nequi indicado, toma una captura e impleméntala como comprobante para validar y dar de baja el retiro de forma definitiva.")
            
            with_df = get_pending_withdrawals()
            
            if len(with_df) == 0:
                st.info("🎉 ¡Al día! No hay solicitudes de retiro pendientes de pago.")
            else:
                for idx, row in with_df.iterrows():
                    with st.expander(f"💸 Retiro #{row['id']} - Usuario: {row['fullname']} ({row['user_code']})"):
                        col_w_info, col_w_pay = st.columns([1, 1])
                        
                        with col_w_info:
                            st.markdown(f"""
                            <div class="card" style="border-left: 3px solid #ffd700;">
                                <p><b>Usuario Solicitante:</b> {row['fullname']} (@{row['username']})</p>
                                <p><b>Código de Billetera:</b> <code style="color:#10b981;">{row['user_code']}</code></p>
                                <p><b>Cuenta Nequi a Transferir:</b> <span style="color:#ffd700; font-weight:bold; font-size:1.2rem;">{row['nequi_number']}</span></p>
                                <p><b>Monto de Retiro Total:</b> ${row['amount_cop']:,.0f} COP</p>
                                <p><b>Comisión Operativa (2%):</b> ${row['fee_cop']:,.0f} COP</p>
                                <p><b>Monto Neto a Enviar:</b> <span style="color:#10b981; font-weight:bold; font-size:1.3rem;">${row['net_cop']:,.0f} COP</span></p>
                                <p><b>Fecha de Solicitud:</b> {row['timestamp']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        with col_w_pay:
                            st.subheader("Subir Soporte Nequi y Confirmar Pago")
                            with st.form(f"admin_confirm_withdrawal_{row['id']}"):
                                with_receipt = st.file_uploader("Adjunta captura de pantalla de transferencia de Nequi realizada:", type=["jpg", "jpeg", "png"], key=f"w_receipt_{row['id']}")
                                
                                col_btn_app, col_btn_rej = st.columns(2)
                                with col_btn_app:
                                    submit_app = st.form_submit_button("Confirmar y Enviar Retiro")
                                    if submit_app:
                                        if not with_receipt:
                                            st.error("⚠️ Debes subir la captura de la transferencia de Nequi antes de confirmar.")
                                        else:
                                            try:
                                                receipt_bytes = with_receipt.read()
                                                success, msg = approve_withdrawal(row['id'], receipt_bytes)
                                                if success:
                                                    st.success("¡Pago de retiro confirmado y comunicado con éxito!")
                                                    st.balloons()
                                                    st.rerun()
                                                else:
                                                    st.error(msg)
                                            except Exception as e:
                                                st.error(f"Error procesando la aprobación: {str(e)}")
                                with col_btn_rej:
                                    submit_rej = st.form_submit_button("Rechazar y Reembolsar COP")
                                    if submit_rej:
                                        if reject_withdrawal(row['id']):
                                            st.warning("Retiro rechazado. Los fondos han sido reembolsados al usuario de inmediato.")
                                            st.rerun()
                                
        with tab_store:
            st.subheader("🛍️ Gestión de Pedidos de la Tienda Alianza")
            st.write("Procesa las compras de los usuarios de la tienda. Puedes entregar el código de activación (PIN) o aprobar la activación VIP.")
            
            store_claims_df = get_pending_store_purchases()
            
            if len(store_claims_df) == 0:
                st.info("🎉 ¡Al día! No hay pedidos de tienda pendientes de entrega.")
            else:
                for idx, row in store_claims_df.iterrows():
                    with st.expander(f"🛍️ Pedido #{row['id']} - {row['name']} - Usuario: {row['fullname']} ({row['user_code']})"):
                        st.markdown(f"""
                        <div class="card" style="border-left: 3px solid #10b981;">
                            <p><b>Artículo comprado:</b> <span style="color:#10b981; font-weight:bold;">{row['name']}</span> ({row['item_type']})</p>
                            <p><b>Usuario:</b> {row['fullname']} (@{row['username']})</p>
                            <p><b>Código de Billetera:</b> <code>{row['user_code']}</code></p>
                            <p><b>Tokens SD Descontados:</b> <span style="color:#ffd700; font-weight:bold;">{row['price_sd']:,.4f} SD</span></p>
                            <p><b>Fecha de Compra:</b> {row['timestamp']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if row['item_type'] == 'MEMBERSHIP':
                            st.write("💡 Este artículo es una Membresía VIP. Al aprobarlo, se le activarán las comisiones reducidas (1%) y bonos (25%) automáticamente.")
                            col_app_s, col_rej_s = st.columns(2)
                            with col_app_s:
                                if st.button("Aprobar y Activar VIP", key=f"app_store_{row['id']}"):
                                    success, msg = deliver_store_purchase(row['id'], "VIP_ACTIVATED")
                                    if success:
                                        st.success(msg)
                                        st.rerun()
                                    else:
                                        st.error(msg)
                            with col_rej_s:
                                if st.button("Rechazar y Reembolsar SD", key=f"rej_store_vip_{row['id']}"):
                                    if reject_store_purchase(row['id']):
                                        st.warning("Compra rechazada y tokens reembolsados.")
                                        st.rerun()
                        else:
                            with st.form(f"deliver_pin_form_{row['id']}"):
                                pin_code = st.text_input("Ingresa el PIN / Código de Activación / Mensaje:", placeholder="Ej. NF-8492-9482-PK19")
                                col_app_s, col_rej_s = st.columns(2)
                                with col_app_s:
                                    submit_deliv = st.form_submit_button("Entregar y Notificar Código")
                                    if submit_deliv:
                                        if not pin_code:
                                            st.error("⚠️ Debes proporcionar el Pin/Código para entregarlo al usuario.")
                                        else:
                                            success, msg = deliver_store_purchase(row['id'], pin_code)
                                            if success:
                                                st.success(msg)
                                                st.rerun()
                                            else:
                                                st.error(msg)
                                with col_rej_s:
                                    submit_rej_store = st.form_submit_button("Rechazar y Reembolsar SD")
                                    if submit_rej_store:
                                        if reject_store_purchase(row['id']):
                                            st.warning("Compra rechazada y tokens reembolsados.")
                                            st.rerun()

        with tab_referrals:
            st.subheader("👥 Gestión de Comisiones por Referidos")
            st.write("Cada vez que un usuario que fue invitado realiza una compra y es aprobada, se calcula un 20% de comisión para su referidor. Valida y autoriza el pago aquí.")
            
            ref_rewards_df = get_pending_referral_rewards()
            
            if len(ref_rewards_df) == 0:
                st.info("🎉 ¡Al día! No hay comisiones de referidos pendientes de pago.")
            else:
                for idx, row in ref_rewards_df.iterrows():
                    with st.expander(f"👥 Comisión #{row['id']} - Referidor: {row['referrer_name']} ({row['referrer_code']})"):
                        st.markdown(f"""
                        <div class="card" style="border-left: 3px solid #10b981;">
                            <p><b>Referidor (Beneficiario):</b> {row['referrer_name']} (Billetera: <code style="color:#10b981;">{row['referrer_code']}</code>)</p>
                            <p><b>Referido (Comprador):</b> {row['referred_name']} (Billetera: <code>{row['referred_code']}</code>)</p>
                            <p><b>Monto de Compra:</b> <span style="color:#ffffff; font-weight:bold;">{row['purchase_amount_sd']:,.4f} SD</span></p>
                            <p><b>Comisión Pendiente (20%):</b> <span style="color:#ffd700; font-weight:bold; font-size:1.15rem;">{row['reward_amount_sd']:,.4f} SD</span></p>
                            <p><b>Fecha de Registro:</b> {row['timestamp']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_pay, col_dec = st.columns(2)
                        with col_pay:
                            if st.button("Aprobar y Enviar Comisión", key=f"pay_ref_{row['id']}"):
                                success, msg = approve_referral_reward(row['id'])
                                if success:
                                    st.success(f"¡Comisión de {row['reward_amount_sd']:,.4f} SD pagada exitosamente!")
                                    st.rerun()
                                else:
                                    st.error(msg)
                        with col_dec:
                            if st.button("Rechazar Comisión", key=f"rej_ref_{row['id']}"):
                                if reject_referral_reward(row['id']):
                                    st.warning("Comisión de referidos cancelada.")
                                    st.rerun()

        with tab_fees:
            st.subheader("📊 Comisiones de la Plataforma (2% por Retiros)")
            st.write("La plataforma recauda un **2% de comisión** en pesos colombianos (COP) por cada retiro aprobado. Por políticas de seguridad, estas comisiones quedan **bloqueadas por 24 horas** a partir de la aprobación del retiro y posteriormente quedan libres para ser reclamadas por el propietario.")
            
            # Obtener resumen de comisiones
            total_fees, locked_fees, available_fees = get_platform_fees_summary()
            
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #3b82f6;">
                    <div class="metric-title">Comisiones Totales Históricas</div>
                    <div class="metric-value" style="color: #3b82f6;">${total_fees:,.0f} COP</div>
                    <div class="metric-sub">Comisiones recaudadas en total</div>
                </div>
                """, unsafe_allow_html=True)
            with col_f2:
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #ef4444;">
                    <div class="metric-title">🔒 Comisiones Bloqueadas (24 Horas)</div>
                    <div class="metric-value" style="color: #ef4444;">${locked_fees:,.0f} COP</div>
                    <div class="metric-sub">Bajo resguardo de seguridad</div>
                </div>
                """, unsafe_allow_html=True)
            with col_f3:
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #10b981;">
                    <div class="metric-title">🔓 Comisiones Liberadas / Retirables</div>
                    <div class="metric-value" style="color: #10b981;">${available_fees:,.0f} COP</div>
                    <div class="metric-sub">Listas para ser transferidas a tu balance</div>
                </div>
                """, unsafe_allow_html=True)
                
            # Botón para reclamar
            if available_fees > 0:
                if st.button("Reclamar y Acreditar Comisiones Liberadas"):
                    success, msg = claim_platform_fees()
                    if success:
                        st.balloons()
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.info("ℹ️ No hay comisiones liberadas pendientes por reclamar en este momento. Las comisiones bloqueadas se liberarán automáticamente después de 24 horas de la aprobación de su respectivo retiro.")
                
            # Tabla de registros de comisiones
            st.subheader("📋 Historial de Comisiones por Retiro")
            df_fees_list = get_approved_withdrawals_fees()
            
            if len(df_fees_list) == 0:
                st.info("No hay registros de comisiones recaudadas todavía.")
            else:
                def calculate_remaining_time(approved_at_str):
                    if not approved_at_str:
                        return "🔓 Liberado"
                    try:
                        approved_time = datetime.strptime(approved_at_str, "%Y-%m-%d %H:%M:%S")
                        release_time = approved_time + timedelta(hours=24)
                        now = datetime.utcnow()
                        if now < release_time:
                            remaining = release_time - now
                            hours, remainder = divmod(remaining.seconds, 3600)
                            minutes, _ = divmod(remainder, 60)
                            return f"🔒 Bloqueado ({hours}h {minutes}m restantes)"
                        else:
                            return "🔓 Liberado"
                    except Exception:
                        return "🔓 Liberado"
                
                df_fees_list['Tiempo de Bloqueo'] = df_fees_list['approved_at'].apply(calculate_remaining_time)
                df_fees_list['Monto del Retiro'] = df_fees_list['amount_cop'].apply(lambda x: f"${x:,.0f} COP")
                df_fees_list['Comisión Recaudada (2%)'] = df_fees_list['fee_cop'].apply(lambda x: f"${x:,.0f} COP")
                df_fees_list['Estado del Saldo'] = df_fees_list.apply(
                    lambda r: "Claimed (Reclamado)" if r['fee_status'] == 'CLAIMED' else r['Tiempo de Bloqueo'], axis=1
                )
                
                df_fees_display = df_fees_list[['approved_at', 'fullname', 'user_code', 'Monto del Retiro', 'Comisión Recaudada (2%)', 'Estado del Saldo']]
                df_fees_display.columns = ['Fecha Aprobación', 'Usuario', 'Código Billetera', 'Monto del Retiro', 'Comisión Recaudada', 'Estado / Bloqueo']
                st.dataframe(df_fees_display, use_container_width=True)

        with tab_messenger:
            st.subheader("🚚 Control de Operaciones de Mensajería y Móviles")
            st.write("Monitorea todos los pagos de envíos entre clientes y conductores, así como el recaudo de cuotas semanales.")
            
            df_all_m = get_all_movil_payments()
            
            if len(df_all_m) == 0:
                st.info("No hay transacciones de mensajería registradas en el sistema.")
            else:
                df_all_m_display = df_all_m.copy()
                df_all_m_display['Tipo de Pago'] = df_all_m_display['payment_type'].apply(
                    lambda t: "📦 Pago de Envío" if t == 'SHIPPING_PAYMENT' 
                    else ("💳 Cuota Semanal (SD)" if t == 'WEEKLY_FEE_SD' else "💳 Cuota Semanal (COP)")
                )
                df_all_m_display['Cliente'] = df_all_m_display.apply(lambda r: f"{r['customer_name']} ({r['user_code']})", axis=1)
                df_all_m_display['Destino'] = df_all_m_display.apply(
                    lambda r: "Admin / Maestra" if r['target_code'] == '99999' else f"{r['target_name']} ({r['target_code']})", axis=1
                )
                df_all_m_display['Monto (SD)'] = df_all_m_display['amount_sd'].apply(lambda x: f"{format_num(x)} SD")
                df_all_m_display['Valor (COP)'] = df_all_m_display['amount_cop'].apply(lambda x: f"${x:,.0f} COP")
                df_all_m_display['Mensaje'] = df_all_m_display['message'].apply(lambda x: str(x) if x else "Ninguno")
                
                df_all_m_display = df_all_m_display[['timestamp', 'Tipo de Pago', 'Cliente', 'Destino', 'Monto (SD)', 'Valor (COP)', 'Mensaje']]
                df_all_m_display.columns = ['Fecha/Hora', 'Tipo de Pago', 'Móvil / Emisor', 'Conductor / Destino', 'Tokens SD', 'Pesos Colombianos', 'Mensaje/Detalle']
                st.dataframe(df_all_m_display, use_container_width=True)


        with tab_broadcast:
            st.subheader("📢 Enviar Comunicado Global a todos los Usuarios")
            st.write("Escribe un mensaje que desees difundir de forma masiva a todos los usuarios registrados en sus bandejas de entrada (Notificaciones).")
            
            with st.form("broadcast_form"):
                broadcast_msg = st.text_area(
                    "Contenido del Mensaje (Soporta HTML básico como <b> o emojis 🚀)", 
                    placeholder="Ej. 🚀 <b>¡Atención!</b> El valor del token SIAD (SD) ha subido un 10% hoy. ¡Revisa tu balance!",
                    height=150
                )
                submit_b = st.form_submit_button("📢 Difundir Comunicado")
                
                if submit_b:
                    if not broadcast_msg.strip():
                        st.error("⚠️ El mensaje no puede estar vacío.")
                    else:
                        broadcast_notification(broadcast_msg)
                        st.success("🎉 ¡Comunicado global enviado exitosamente a todos los usuarios!")
                        st.balloons()
                        st.rerun()

        with tab_settings:
            st.subheader("⚙️ Configuración Técnica del Token y Pasarela Nequi")
            
            # --- SECCIÓN ADICIONAL: EDITAR TIENDA ---
            st.markdown("---")
            st.subheader("🛍️ Editar Precios e Información de la Tienda")
            st.write("Modifica el nombre, descripción y costo en tokens SIAD (SD) de las membresías y artículos que los usuarios compran en la tienda Alianza.")
            
            # Cargar artículos de la tienda
            conn_items = get_db_connection()
            store_items_list = pd.read_sql_query("SELECT id, name, description, price_sd, item_type FROM store_items", conn_items)
            conn_items.close()
            
            for idx_i, item_row in store_items_list.iterrows():
                i_id = item_row['id']
                i_name = item_row['name']
                i_type = item_row['item_type']
                i_price = float(item_row['price_sd'])
                i_desc = item_row['description']
                
                type_label = "🏆 Membresía VIP Alianza" if i_type == 'MEMBERSHIP' else "🎁 Tarjeta de Regalo / Pin"
                with st.expander(f"✏️ Editar: {i_name} ({type_label})"):
                    with st.form(f"edit_store_item_form_{i_id}"):
                        edit_name = st.text_input("Nombre del Artículo", value=i_name)
                        edit_desc = st.text_area("Descripción", value=i_desc, height=80)
                        edit_price = st.number_input("Costo del Artículo (SD)", value=i_price, min_value=0.0001, format="%.4f")
                        submit_item_edit = st.form_submit_button(f"Guardar Cambios de {i_name}")
                        
                        if submit_item_edit:
                            if not edit_name.strip() or not edit_desc.strip():
                                st.error("⚠️ El nombre y la descripción no pueden estar vacíos.")
                            else:
                                update_store_item_price(i_id, edit_price, edit_name, edit_desc)
                                st.success(f"✅ ¡Se han guardado los cambios para '{edit_name}' con éxito!")
                                st.rerun()
            st.markdown("---")
            
            # Verificación explícita de seguridad: Sólo la cuenta de administrador principal (@admin o wallet_code 99999) puede editar el Nequi global de recepción de pagos.
            is_admin_user = (st.session_state.username == 'admin' or st.session_state.wallet_code == '99999')
            if not is_admin_user:
                st.warning("⚠️ Solamente el usuario administrador principal (@admin) puede editar la configuración global de la plataforma y el número de Nequi oficial.")
                st.info(f"<b>Nequi Oficial del Administrador para Recibir Pagos:</b> {token['nequi_number']}")
            else:
                st.write("Desde aquí personalizas las características de tu propia criptomoneda y el canal de pago de forma global.")
                with st.form("settings_form"):
                    new_name = st.text_input("Nombre de la Criptomoneda", value=token['name'])
                    new_symbol = st.text_input("Símbolo del Token", value=token['symbol'], max_chars=10)
                    new_contract = st.text_input("Dirección de Contrato (Smart Contract)", value=token['contract'])
                    new_price = st.number_input("Valor en USD de cada Token (USD)", value=token['price_usd'], min_value=0.000001, format="%.6f", step=0.01)
                    new_nequi = st.text_input("Número de Cuenta NEQUI Oficial para Recibir Pagos", value=token['nequi_number'])
                    submit_s = st.form_submit_button("Guardar Configuración Técnica")
                    
                    if submit_s:
                        if not (new_name and new_symbol and new_contract and new_nequi):
                            st.error("Todos los campos de configuración son obligatorios.")
                        else:
                            update_token_settings(new_name, new_symbol, new_contract, new_price, new_nequi)
                            st.success("¡Configuración general guardada con éxito!")
                            st.rerun()
