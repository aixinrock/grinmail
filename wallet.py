import pexpect,re,time


class GrinWallet():
     def __init__(self,password):
          self.password = password
          

     def terminal(self,params):
          command = 'grin-wallet ' + params
          child = pexpect.spawn(command)
          child.expect('Password:')
          child.sendline(self.password)
          child.expect(pexpect.EOF)
          result = child.before.decode('utf-8')
          return result

     def terminal_s(self,params,slatepack):
          command = 'grin-wallet ' + params
          child = pexpect.spawn(command)
          child.expect('Password:')
          child.sendline(self.password)
          child.expect('message:')
          child.sendline(slatepack)
          child.expect(pexpect.EOF)
          result = child.before.decode('utf-8')
          return result

     def info(self):
          result = self.terminal('info')
          
          total_pattern = re.compile(r'Confirmed Total.*(\d+\.\d+)')
          total = re.search(total_pattern,result).group(1)
          confirmation_pattern = re.compile(r'Awaiting Confirmation.*(\d+\.\d+)')
          confirmation = re.search(confirmation_pattern,result).group(1)
          finalization_pattern = re.compile(r'Awaiting Finalization.*(\d+\.\d+)')
          finalization = re.search(finalization_pattern,result).group(1)
          locked_pattern = re.compile(r'Locked by previous transaction.*(\d+\.\d+)')
          locked = re.search(locked_pattern,result).group(1)
          spendable_pattern = re.compile(r'Currently Spendable.*(\d+\.\d+)')
          spendable = re.search(spendable_pattern,result).group(1)

          return (total,confirmation,finalization,locked,spendable)

     def confirmed_total(self):
          return self.info()[0]

     def awaiting_confirmation(self):
          return self.info()[1]

     def awaiting_finalization(self):
          return self.info(2)

     def locked(self):
          return self.info(3)

     def currently_spendable(self):
          return self.info(4)

     def address(self):
          result = self.terminal('address')

          pattern = re.compile(r'grin.*')
          addr = re.search(pattern,result).group()
          return addr

     def cancel(self,id=0):
          stop = False
          trans_nums = ''
          if id:
               params = 'cancel -i ' + str(id)
               result = self.terminal(params)
               res = result.split('\n')[-2]
               return res
          while not stop:
               params = 'cancel -i ' + str(id)
               result = self.terminal(params)
               id += 1
               if "doesn't exist" in result:
                    stop = True
               if 'successfully' in result:
                    trans_nums += f'{id} '
          res = f'Transaction {trans_nums} canceled successfully!'
          return res
          
     def receive(self,slatepack):
          result = self.terminal_s('receive -m',slatepack)

          pattern = re.compile(r'/home.*?S2.slatepack')
          slate_file = re.search(pattern,result).group()
          with open(slate_file,'r') as f:
               slate = f.read()
          return slate

     def scan(self):
          child = pexpect.spawn('grin-wallet scan')
          child.expect('Password:')
          child.sendline(self.password)
          
     def send(self,amount):
          result = self.terminal('send ' + str(amount))
          pattern = re.compile(r'/home.*?S1.slatepack')
          slate_file = re.search(pattern, result).group()
          with open(slate_file,'r') as f:
               slatepack = f.read()
          return slatepack

     def finalize(self,slatepack):
          result = self.terminal_s('finalize',slatepack)
          return result

if __name__ == '__main__':
     start = time.time()
     wallet = GrinWallet('2pingping')
     confirmed_total,awaiting_confirmation,awaiting_finalization,locked,currently_spendable = wallet.info()


     print(f'''               ————————————Grin余额信息————————————

               总 资 产 ：  {confirmed_total}
               可花费额 ：  {currently_spendable}
               上链确认 ：  {awaiting_confirmation}
               等待完结 ：  {awaiting_finalization}
               交易锁定 ：  {locked}

               ————————————————————————————————————
          ''')
     
     print(wallet.address())
     print(wallet.cancel(85))
     s1 = 'BEGINSLATEPACK. QiapnaVHQxYuuyH GYEqTScyBQSQG1n bHWsaZNTgHwBjx3 A4RoSqjtV7H6nu7 Xojry4dZ6w7Sj3a XEtxJjbza5W7zzX QhpLfjYFa8v38az EsC547t17Hm1zAC TnjqBXw54EYks43 BazAenyAHq1Rjyv YpurqAf4jQqmiEW MPjMCa12td4jEBj xYQHrbVmueayQt9 AQZ9wRAq4yhas3E kaRmi2spP3i6JGV VABVBJ4kHTpf3RS 2waJFct7xXJRnoe 283Ke6ZFFrvYtRw 7t4WJ692vXuHth2 sSSmgjRZ1Jz7C5N z9NC8w. ENDSLATEPACK.'
     #print(wallet.receive(s))
     #print(wallet.scan())
     #print(wallet.send(0.2))
     s3 = 'BEGINSLATEPACK. 9TK3SXvZX8xf3hj N634sLdbhKsFRbL kf6XE84wh96hNay LoKmLctMbA3LQoq a6DGyYeH6c5iiKC ZFw2A8wCj7uTuAx uqVMvHesuDaXbq2 rY9S3J8vwZS7AVm eq4nejf1mHDuDnM wuRypCVGYWujZd7 eJaYYYNMJC1qtXd t3WNFLdt48AzXWP TK2TjiE72t14ZtF m3y4jdaHmeJRhvt mBtJSfQ9gyy8keS yaFz7tzJteBqJVV m2WEM6NWKCYMdUm PuRxGbBMMa35nTP e9K4gjnXEi84t9L 3as5EN1qQi8bcwm DtuFe6nsn8b6TjF qCFropSAFkxEsQT mK1nZ5ks7uQmmGx FKJxp1uatGC67zs 8Tb113fRW9RLQiD uarJ969zDj8EsE5 aZBhM2whq2Z4T3U pytxcXFsuUNbE7C QJ7UxB9JT3x1xZX KXdup86d2VZB147 8W6F96GuSDFytJD nqQkHAorwwzSh5K H1cRENghteVD9Tu tm7Jpodzs1mcLQE nWiKqLZb8FJYiva RMhnJYQsaSpT5xq A6iGkWstUrEfAMi n5fec1P5cScPD9y qpZG3eGUgcsZ4GD inQWN9EGDyVYrXG bnjB6Fu1twUBw4F koQdSW3xEVGJxCR bdBpNZjumDkYcY5 N96GmWJ9Whq89xq XFZufdWJMnoEKxv tMJ6T4z6L5AeN1u TqgEkxaXrFKyyuP DWgupxr4UTnpwnB SAuKMigxBxyKG6j Jb35dp6pQj4BwEv VbsMNH7pLipjUkj rAhkAmpb9REZQiF q43oDYJN531zUru jeURxKPQTtoeNnH 5be5EEkE2qigVS4 QfxXDiE39SX6Nxi t6oKB2XeJtoY9yK ToNF2p7qLmvSuLj aP8JhjjvxS2jwjn 21k1VwAfyqAUvg3 mKRysxU2wLUWEeu XXDmhGPNYRbxwnA wNU8NMfC52qZDD3 6su4jFTeXFbrUoy cFyRF1dQ6y86hjw 5o1c8HgE47cBMtQ Ny3TcVRtVkHCGP4 KWeM1dFstyJuVz6 jWn5pSMSRLCDDUd 3Z2KkYrNnX4pCDe Lx8gJnooWMySZmK GJfARa4yT3dHArV mDCPUGXCJZfjb1K FUUNn6eDExUiMeA 9CbGb63YakwZavb 1pQPzkZYjv2srtZ MZSTRGaVAj2h1dR Erf9uVZqWRs57vq hszQrLXdJTLPGvn RW65wuEHDF6Ny29 QhhNRQr5dLNXDgT 2WKYfLwb1gGqMHq osRqGKQwHRx5bNd xm2hCeT4TJiUtop 2nivYAv9v93Fi9o qCqKRQGRXs72cU9 znqtsXDbSdEzzz1 FPXHuGNZP9Zhv1D wAQjSSwQXChKgJh AkjvePANvQsQUyu j4hZAf2KxGgAHKH cDUxAnpCHCfTxFp EvovJrW9W4aRAPm 5Rm5MQZRvCzDEof tHhykKLxyHRuUPy MbEpYBhZMWFfCWG pqcFpi85nPDDZwZ YEUUdvz3pQGkgb1 2766jzLvu33KjPA EjSDLaNYzLXtP8z RmEti4oaX3QkXLy mxF1wRvYnmyVmtT DQo2LjkJBB5e4qn xu2tFEFbvaKqK6k DbUm6HBD94v5GRP G7HVnkFNWTCMBss SSZQoWJkGqJbHzD YSHKXp4pS5UCkW1 ddsjRpLdXDYnWp5 ninRtkYt2FsQ4hZ TWKmvsNiK6uW2FU 8939oHhRDX3BDni 7QAKGJMWUFiDJkH jRPfBztSNirtpGU sYLyKsw7sU8nWiD DvLDf7HWTCNeH2v kszHuNkiBTCRHBR XuWSqK5F9W4UDtU Brad5r4Uz8NFbeR NN1G6tSdtH1XVey chCNksabXCPj57u xWt1V5xZoYHY6js QL2Eztmox2hW6dD 1irZMH8XbxCYmbC wdL5C783Uy3TPRy icjDAgJrLx87U7T WPekGaMhwzQwz6c zxHpk7Z1hxQmeKF Tvt3V9jKVievmnG thM9WcEFtNo9ksb Ttwme1EjK3Cqbne 2By173ZRiLfmLaQ cZw6MLRna1xC71D DBXj3DKGXAgdYKB HUyxNXKGq2Lr76y wBU9CoivnHf9da9 L1aEABsY7yPsGjk oqJTuY2Q2HhKgsP Ty1f3NEGzLP1DB7 27Qm79A1kNyK1fP ciJ7sdusxEuqQBD 7qzxdp5MDft4sSE pBFDSxM55SbLwtG F1nKEL5b64ZbNPa JZ3DH6Faiqz3cLx no87iuCodSRxDMb KekiXspwPHt6DV8 P3pZQaEdxHXBb3J dNKAo4Jt4hNncBE d825kRm6vEfWtZe cvwg2UH9XyTLVfW EY1MtTE4cZNeT2J oSSqjGhdxD9XCmK MY8Hcf4GEfW1LAg sDnrh2cygDduWV8 QdfC8ejNeBQNQvt qmoFhiS4brtXYzS 4GBYXRXtTcSKYm8 tdATuX1ibJMiCXC m4nsp4ZBreSfQkz jzzFjDZdDtE6CLS EU7TNdzacqrF6oy TDjepzPxE5evkGJ 1ePhuQVf3126Kih t3uqw66mHPue38b jnV7hygSim486Cb 8oy1QFrisaYUB2D wqytq6crkLuPJ4Y PFT6LTbesDeS8Uq 44MW7xo5ZFBaW2t rjWabB8x3CYLVez kj2zN5W7TtWjXhp WNZvVdEKAUVFWxN 4nGBARMdFZptUau jqQVJAMxKrr. ENDSLATEPACK.'
     print(wallet.finalize(s3))
     print(time.time() - start)