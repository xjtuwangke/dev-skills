# Pricing And Promotions Reference

## Quote Behavior
- Catalog unit price times quantity creates subtotal.
- Enterprise customers can receive loyalty discount.
- Coupon `SAVE20` can apply a 20 percent discount.
- Pricing chooses the larger discount, then applies tax.

## Promotion Behavior
- `SAVE20` is eligible for non-legacy SKUs.
- Enterprise customers have fallback eligibility for non-matching coupons.
- Legacy SKUs starting with `OLD` should be treated carefully when adding promotion behavior.

## Tables
- `price_lists`
- `price_list_items`
- `tax_rates`
- `promotion_campaigns`
- `coupons`
- `coupon_redemptions`

## Code
- `PricingService`
- `PromotionService`
- `MoneyMapper`
- `CatalogMapper`
