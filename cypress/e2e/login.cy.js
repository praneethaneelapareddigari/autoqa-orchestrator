describe('Login flow', () => {
  it('visits kitchen sink and checks content', () => {
    cy.visit('/')
    cy.contains('Kitchen Sink').should('exist')
  })
})
