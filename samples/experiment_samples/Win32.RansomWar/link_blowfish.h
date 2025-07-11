static unsigned long F(unsigned long x, union symmetric_key *key);
int blowfish_setup(unsigned char *key, int keylen, int num_rounds, union symmetric_key *skey);
void blowfish_ecb_encrypt(unsigned char *pt, unsigned char *ct, union symmetric_key *key);
void blowfish_ecb_decrypt(unsigned char *ct, unsigned char *pt, union symmetric_key *key);