# E-mail on whitelabelmedia.eu (2026-11-04)

`rihards@whitelabelmedia.eu` is a Google Workspace user in the Marketinga Skola Workspace, where whitelabelmedia.eu is a verified secondary domain. SiteGround had no mailboxes on the domain, so moving its mail to Google loses nothing.

## DNS (SiteGround → Site Tools for whitelabelmedia.eu → Domain → DNS Zone Editor)

1. **MX:** Create New Record → MX → "Switch to Google MX records". This replaces the three `mx*.antispam.mailspamprotection.com` records.
2. **SPF:** edit the TXT record on `whitelabelmedia.eu` that starts with `v=spf1` to:
   `v=spf1 include:_spf.google.com ~all`
   (Nothing sends as @whitelabelmedia.eu from SiteGround; the site's form e-mails go out through n8n's Gmail.)
3. **DKIM:** Create New Record → TXT, name `google._domainkey`, value:
   `v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA86xd5nX9UXBXiTM3cA7B86XsjTexVnirXX5f4Z8qKoXW7KwKAgqClgozGPAyE+5FHAf0MSJbrHcwrRzFMJ6sfKudJ6aEL5oMU7iManSNj2Fl9g/D0ewtrZW1KwUOxbfb1BNzTf6C9DAZyRrXcAZ0Kb62BKZ3bIvx5RCMTYUNPxTlqqohoAzJgHPZ6eQj6G9jj9cBDPYuyIE0QSkqbGndgnCWggdNWHDL4HhT9WO86CTJg/0bdLfkbFsugaLHb/LjblygrcWXaxcAE4/l3WCeNQl+EWnSuhFWaVgbfH4KG0OTQzEwFKTSG3pv1fUCeq/b0IrA6s3Ds/lPRU2K98BGPwIDAQAB`
   Then in Google Admin → Apps → Google Workspace → Gmail → Authenticate email → whitelabelmedia.eu → **Start authentication**.
4. **DMARC:** keep the existing `_dmarc` record (`v=DMARC1; p=quarantine; aspf=r; adkim=r`).

Leave the A records, `ssh`, `www` and the Google site-verification TXT alone: the website and the deploy depend on them.

## Check

```bash
dig +short MX whitelabelmedia.eu
```
```bash
dig +short TXT google._domainkey.whitelabelmedia.eu
```

## Cold e-mail from the main domain

The owner chose to send outreach from `rihards@whitelabelmedia.eu` instead of a separate domain. Fine at the current volume (a few hand-written e-mails a day). If outreach grows past about 50 new contacts a week, move cold sending to a second domain so complaints can't hurt the site's domain.
